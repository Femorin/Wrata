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
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from mistralai.client import Mistral

BOT_TOKEN       = os.getenv("BOT_TOKEN")
CHAT_ID         = os.getenv("CHAT_ID")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
HOTKEY          = os.getenv("HOTKEY", "f8")

_mistral = Mistral(api_key=MISTRAL_API_KEY)


def make_screenshot() -> io.BytesIO:
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[0])
        img  = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        buf  = io.BytesIO()
        img.save(buf, "JPEG", quality=90, optimize=True)
        buf.seek(0)
        return buf


def ask_pixtral(buf: io.BytesIO) -> str:
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
                    "text": "На скриншоте есть вопрос или задание. Ответь на него подробно в 5 предложений не сильно больших. Если вопроса нет — опиши что видишь. Если вопрос есть - пиши сразу правильный вариант ответа и пояснение на 5 предложений."
                }
            ]
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
            buf    = make_screenshot()
            answer = ask_pixtral(buf)
        except Exception as e:
            answer = f"Ошибка Pixtral: {e}"
        send_message(answer)

    threading.Thread(target=worker, daemon=True).start()


def build_icon() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    ImageDraw.Draw(img).rectangle([3, 3, 12, 12], fill=(50, 50, 50, 200))
    return img


def main():
    keyboard.add_hotkey(HOTKEY, on_hotkey, suppress=True)

    def quit_app(icon, _):
        keyboard.unhook_all()
        icon.stop()

    pystray.Icon(
        name="s",
        icon=build_icon(),
        title="",
        menu=pystray.Menu(item("Выход", quit_app)),
    ).run()


if __name__ == "__main__":
    main()
