# Wrata — скриншот → ИИ → Telegram

**WRATA — СПИШИ АБСОЛЮТНО ВСЕ!**
Нажми горячую клавишу — скриншот уйдёт в нейросеть, она ответит на вопрос с экрана и пришлёт ответ в Telegram.

При запуске выбираешь модель: **Mistral** или **Gemini**.

---

## Установка

### Windows

**1. Установи зависимости**
```
pip install -r requirements.txt
pip install mistralai python-dotenv
```

**2. Создай `.env`**
```
cp .env.example .env
```
Заполни своими ключами (см. раздел «Где брать ключи»).

**3. Запусти**

Двойной клик по **`start.vbs`** — запускает полностью невидимо, без консоли и иконки в трее.

Или через терминал:
```
python screen_tg.py
```

---

### macOS

**1. Установи зависимости**
```bash
pip3 install -r requirements_mac.txt
```

**2. Системные разрешения (один раз)**

Системные настройки → Конфиденциальность и безопасность:
- **Специальные возможности** → добавить Terminal
- **Запись экрана** → добавить Terminal

Без этого хоткеи и скриншоты не работают.

**3. Создай `.env`**
```bash
cp .env.example .env
```

**4. Запусти**
```bash
chmod +x start_mac.command
```
Затем двойной клик по **`start_mac.command`**.

---

### Linux

> Работает только на **X11**. Wayland не поддерживается.

**1. Системные пакеты**
```bash
# Ubuntu/Debian
sudo apt install python3-tk python3-xlib

# Arch
sudo pacman -S python-tkinter python-xlib

# Fedora
sudo dnf install python3-tkinter python3-xlib
```

**2. Установи зависимости**
```bash
pip3 install -r requirements_linux.txt
```

**3. Создай `.env`**
```bash
cp .env.example .env
```

**4. Запусти**
```bash
chmod +x start_linux.sh
./start_linux.sh
```

> Если используешь Wayland — запускай так: `GDK_BACKEND=x11 ./start_linux.sh`

---

## Где брать ключи

### Telegram Bot Token (`BOT_TOKEN`)
1. Открой Telegram → [@BotFather](https://t.me/BotFather)
2. Отправь `/newbot`, придумай имя и юзернейм
3. Скопируй токен вида `1234567890:AAH...` в `BOT_TOKEN`

### Telegram Chat ID (`CHAT_ID`)
1. Напиши что-нибудь своему боту
2. Открой [@userinfobot](https://t.me/userinfobot) → `/start`
3. Скопируй свой ID в `CHAT_ID`

### Mistral API Key (`MISTRAL_API_KEY`)
1. [console.mistral.ai](https://console.mistral.ai) → регистрация
2. **API Keys** → **Create new key**
3. Скопируй в `MISTRAL_API_KEY`

> Есть бесплатный тир без привязки карты.

### OpenRouter API Key (`OPENROUTER_API_KEY`) — для Gemini
1. [openrouter.ai/keys](https://openrouter.ai/keys) → регистрация
2. Создай ключ, скопируй в `OPENROUTER_API_KEY`

> Нужен только если планируешь использовать режим Gemini.

---

## Выбор модели

При каждом запуске появляется окно с выбором:

- **Mistral** — использует `MISTRAL_API_KEY`. Извлекает вопрос через Pixtral, решает через Mistral Large. Ответ — короткий.
- **Gemini** — использует `OPENROUTER_API_KEY`. Gemini решает задачу развёрнуто, затем Mistral сжимает ответ до одной строки в Telegram.

---

## Горячие клавиши

Настраиваются в `.env`:

| Переменная | По умолчанию | Действие |
|---|---|---|
| `HOTKEY` | `f8` | Скриншот → ИИ → Telegram |
| `QUIT_HOTKEY` | `ctrl+alt+shift+q` | Завершить программу |

Примеры значений для `HOTKEY`:
```
HOTKEY=f8
HOTKEY=f12
HOTKEY=ctrl+shift+s
HOTKEY=alt+f9
```

**Закрыть программу:** `Ctrl + Alt + Shift + Q` или завершить процесс `python` / `pythonw.exe` в диспетчере задач.

---

## Файлы

| Файл | Описание |
|---|---|
| `screen_tg.py` | Основной скрипт (Windows / macOS / Linux) |
| `start.vbs` | Запуск на Windows (без консоли) |
| `start_mac.command` | Запуск на macOS |
| `start_linux.sh` | Запуск на Linux |
| `requirements.txt` | Зависимости для Windows |
| `requirements_mac.txt` | Зависимости для macOS |
| `requirements_linux.txt` | Зависимости для Linux |
| `.env` | Твои ключи (не коммитить!) |
| `.env.example` | Шаблон `.env` |
