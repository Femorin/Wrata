import sys
import io
import os
import threading
import ctypes
import base64

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

BOT_TOKEN       = os.getenv("BOT_TOKEN")
CHAT_ID         = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
HOTKEY          = os.getenv("HOTKEY", "f8")
QUIT_HOTKEY     = os.getenv("QUIT_HOTKEY", "ctrl+alt+shift+q")
SOLVER_MODEL    = os.getenv("SOLVER_MODEL", "mistral-large-latest")

_mistral = Mistral(api_key=MISTRAL_API_KEY)


def make_screenshot() -> io.BytesIO:
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[0])
        img  = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        buf  = io.BytesIO()
        img.save(buf, "JPEG", quality=90, optimize=True)
        buf.seek(0)
        return buf


def extract_question(buf: io.BytesIO) -> str:
    image_b64 = base64.b64encode(buf.read()).decode()
    response = _mistral.chat.complete(
        model="pixtral-12b-2409",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                },
                {
                    "type": "text",
                    "text": (
                        "Извлеки с этого скриншота текст вопроса или задания дословно. "
                        "Если есть варианты ответов — перечисли их тоже. "
                        "Не решай сам, только точно перепиши текст с экрана."
                    )
                }
            ]
        }]
    )
    return response.choices[0].message.content


def solve_question(question: str) -> str:
    response = _mistral.chat.complete(
        model=SOLVER_MODEL,
        messages=[{
            "role": "user",
            "content": (
                f"{question}\n\n"
                "Дай правильный ответ и объясни его в двух предложениях. "
                "Если есть варианты — укажи какой правильный и почему. "
                "Если правильных вариантов несколько, то назови все верные. "
                "ВАЖНО: не используй LaTeX-разметку (\\frac, \\cdot, \\[ и т.п.). "
                "Пиши математику обычным текстом: дроби как 11/3, "
                "степени как 3^10, умножение как ×, корень как √."
            )
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
