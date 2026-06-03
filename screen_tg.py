import sys
import io
import os
import threading
import ctypes
import base64
import tkinter as tk

if sys.platform == "win32":
    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 0
    )

from dotenv import load_dotenv
load_dotenv()

import keyboard
import mss
import requests
from PIL import Image
from mistralai.client import Mistral

BOT_TOKEN          = os.getenv("BOT_TOKEN")
CHAT_ID            = os.getenv("CHAT_ID")
MISTRAL_API_KEY    = os.getenv("MISTRAL_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HOTKEY             = os.getenv("HOTKEY", "f8")
QUIT_HOTKEY        = os.getenv("QUIT_HOTKEY", "ctrl+alt+shift+q")
SOLVER_MODEL       = os.getenv("SOLVER_MODEL", "mistral-large-latest")

# Mistral всегда инициализируется: решает в mistral-режиме, сжимает в gemini-режиме
_mistral = Mistral(api_key=MISTRAL_API_KEY)


def choose_provider() -> str:
    result = ["mistral"]

    root = tk.Tk()
    root.title("Выбор AI модели")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    width, height = 300, 130
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+{(sw - width) // 2}+{(sh - height) // 2}")

    tk.Label(root, text="Выберите AI модель:", font=("Arial", 12)).pack(pady=14)

    frame = tk.Frame(root)
    frame.pack()

    def select(choice):
        result[0] = choice
        root.destroy()

    tk.Button(frame, text="Mistral", width=12,
              command=lambda: select("mistral")).pack(side=tk.LEFT, padx=12)
    tk.Button(frame, text="Gemini", width=12,
              command=lambda: select("gemini")).pack(side=tk.LEFT, padx=12)

    root.protocol("WM_DELETE_WINDOW", lambda: select("mistral"))
    root.mainloop()

    return result[0]


AI_PROVIDER = choose_provider()

if AI_PROVIDER == "gemini":
    from openai import OpenAI
    _openrouter = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    _gemini_model = "google/gemini-2.5-flash"


def make_screenshot() -> io.BytesIO:
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[0])
        img  = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        buf  = io.BytesIO()
        img.save(buf, "JPEG", quality=90, optimize=True)
        buf.seek(0)
        return buf


_EXTRACT_PROMPT = (
    "Извлеки с этого скриншота текст вопроса или задания дословно. "
    "Если есть варианты ответов — перечисли их тоже. "
    "Не решай сам, только точно перепиши текст с экрана."
)

_SOLVE_PROMPT_MISTRAL = (
    "Дай правильный ответ и объясни его в двух предложениях. "
    "Если есть варианты — укажи какой правильный и почему. "
    "Если правильных вариантов несколько, то назови все верные. "
    "ВАЖНО: не используй LaTeX-разметку (\\frac, \\cdot, \\[ и т.п.). "
    "Пиши математику обычным текстом: дроби как 11/3, "
    "степени как 3^10, умножение как ×, корень как √."
)

_SOLVE_PROMPT_GEMINI = (
    "Реши задачу подробно, проверь ответ шаг за шагом. "
    "Убедись что выбран правильный вариант. "
    "Не используй LaTeX: дроби как 11/3, степени как 3^10, умножение как ×."
)

_COMPRESS_PROMPT = (
    "Вот решение задачи:\n\n{solution}\n\n"
    "Если правильных вариантов несколько, то назови все верные. "
    "ВАЖНО: не используй LaTeX-разметку (\\frac, \\cdot, \\[ и т.п.). "
    "Пиши математику обычным текстом: дроби как 11/3, "
    "степени как 3^10, умножение как ×, корень как √."
    "Выдай ТОЛЬКО финальный ответ одной строкой. "
    "Если есть буква варианта — напиши её и значение. Пример: 'Б — 180 см' или 'Д — 42'. "
    "Если вариантов нет — предложением"
    "Никаких объяснений, никаких вычислений."
)


def extract_question(buf: io.BytesIO) -> str:
    image_b64 = base64.b64encode(buf.read()).decode()

    if AI_PROVIDER == "mistral":
        response = _mistral.chat.complete(
            model="pixtral-12b-2409",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                    },
                    {"type": "text", "text": _EXTRACT_PROMPT}
                ]
            }]
        )
        return response.choices[0].message.content
    else:
        response = _openrouter.chat.completions.create(
            model=_gemini_model,
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                    },
                    {"type": "text", "text": _EXTRACT_PROMPT}
                ]
            }]
        )
        return response.choices[0].message.content


def solve_question(question: str) -> str:
    if AI_PROVIDER == "mistral":
        response = _mistral.chat.complete(
            model=SOLVER_MODEL,
            messages=[{
                "role": "user",
                "content": f"{question}\n\n{_SOLVE_PROMPT_MISTRAL}"
            }]
        )
        return response.choices[0].message.content
    else:
        # Gemini думает свободно без ограничений
        response = _openrouter.chat.completions.create(
            model=_gemini_model,
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": f"{question}\n\n{_SOLVE_PROMPT_GEMINI}"
            }]
        )
        return response.choices[0].message.content


def compress_answer(solution: str) -> str:
    """Mistral сжимает развёрнутый ответ Gemini до одной строки."""
    response = _mistral.chat.complete(
        model=SOLVER_MODEL,
        messages=[{
            "role": "user",
            "content": _COMPRESS_PROMPT.format(solution=solution)
        }]
    )
    return response.choices[0].message.content


def send_message(text: str):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text},
            timeout=30,
        )
    except Exception:
        pass


def on_hotkey():
    def worker():
        try:
            buf      = make_screenshot()
            question = extract_question(buf)
            answer   = solve_question(question)
            if AI_PROVIDER == "gemini":
                answer = compress_answer(answer)
            send_message(answer)
        except Exception as e:
            send_message(f"Ошибка: {e}")

    threading.Thread(target=worker, daemon=True).start()


def main():
    _stop = threading.Event()

    keyboard.add_hotkey(HOTKEY, on_hotkey, suppress=True)
    keyboard.add_hotkey(QUIT_HOTKEY, _stop.set, suppress=True)

    _stop.wait()
    keyboard.unhook_all()


if __name__ == "__main__":
    main()
