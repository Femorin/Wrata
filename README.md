# Wrata — скриншот → ИИ → Telegram

**WRATA — СПИШИ АБСОЛЮТНО ВСЕ!**
Нажми горячую клавишу — скриншот уйдёт в нейросеть, она ответит на вопрос с экрана и пришлёт ответ в Telegram.

При запуске выбираешь модель: **Mistral** или **Gemini**.

> **Пользователям macOS:** для вас есть отдельный репозиторий — [https://github.com/ViktorHarko/Molfar](https://github.com/ViktorHarko/Molfar)

---

## Установка с нуля (Windows)

Если ты устанавливаешь первый раз — следуй шагам по порядку.

---

### Шаг 1 — Установи Python

1. Открой [python.org/downloads](https://www.python.org/downloads/) и скачай последнюю версию Python.
2. Запусти установщик.
3. **ВАЖНО:** поставь галочку **"Add Python to PATH"** внизу окна перед тем, как нажать Install.
4. Нажми **Install Now** и дожди завершения.

Проверь, что Python установился — открой **PowerShell** (клавиша Win → напиши `powershell` → Enter) и выполни:
```
python --version
```
Должно написать что-то вроде `Python 3.12.0`.

---

### Шаг 2 — Установи Git

1. Открой [git-scm.com/downloads](https://git-scm.com/downloads) и скачай Git для Windows.
2. Запусти установщик, везде жми **Next**, настройки по умолчанию подойдут.
3. Нажми **Install** и дожди завершения.

---

### Шаг 3 — Скачай программу с GitHub

Открой **PowerShell** и выполни по одной команде:

```
cd Desktop
```
```
git clone https://github.com/Femorin/Wrata.git
```

Появится папка `Wrata` на рабочем столе.

---

### Шаг 4 — Перейди в папку программы

В том же PowerShell:
```
cd Wrata
```

---

### Шаг 5 — Установи зависимости

```
pip install -r requirements.txt
```

Подожди, пока всё установится (может занять минуту-две).

---

### Шаг 6 — Создай файл с ключами

Скопируй шаблон:
```
copy .env.example .env
```

Теперь открой файл `.env` в папке `Wrata` через Блокнот (правая кнопка → **Открыть с помощью → Блокнот**) и заполни свои ключи.

Файл выглядит так:
```
BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
MISTRAL_API_KEY=your_mistral_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
HOTKEY=f8
QUIT_HOTKEY=ctrl+alt+shift+q
```

Замени каждое `your_..._here` на свой реальный ключ. Где их брать — читай раздел **«Где брать ключи»** ниже.

---

### Шаг 7 — Запусти программу

Зайди в папку `Wrata` на рабочем столе, найди файл **`start.vbs`**, нажми правой кнопкой → **Запуск от имени администратора**.

Программа запустится невидимо, без консоли и иконки в трее. После запуска появится маленькое окошко с выбором модели.

---

## Обновление (если уже установлено)

Открой папку `Wrata`, зажми `Shift` + правая кнопка мыши на пустом месте → **Открыть окно PowerShell здесь**, выполни:
```
git pull origin main
pip install -r requirements.txt
```
Затем запусти `start.vbs` правой кнопкой → **Запуск от имени администратора**.

---

## Установка на Linux

> Работает только на **X11**. Wayland не поддерживается.

**1. Установи системные пакеты**
```bash
# Ubuntu/Debian
sudo apt install git python3 python3-pip python3-tk python3-xlib

# Arch
sudo pacman -S git python python-pip python-tkinter python-xlib

# Fedora
sudo dnf install git python3 python3-pip python3-tkinter python3-xlib
```

**2. Скачай программу**
```bash
cd ~
git clone https://github.com/Femorin/Wrata.git
cd Wrata
```

**3. Установи зависимости**
```bash
pip3 install -r requirements_linux.txt
```

**4. Создай `.env`**
```bash
cp .env.example .env
nano .env
```
Заполни ключи (см. раздел «Где брать ключи»).

**5. Запусти**
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
1. Зайди на [console.mistral.ai](https://console.mistral.ai) → зарегистрируйся
2. **API Keys** → **Create new key**
3. Скопируй ключ в `MISTRAL_API_KEY`

> Есть бесплатный тир без привязки карты.

### OpenRouter API Key (`OPENROUTER_API_KEY`) — для Gemini
1. Зайди на [openrouter.ai/keys](https://openrouter.ai/keys) → зарегистрируйся
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
| `screen_tg.py` | Основной скрипт |
| `start.vbs` | Запуск на Windows (без консоли) |
| `start_linux.sh` | Запуск на Linux |
| `requirements.txt` | Зависимости для Windows |
| `requirements_linux.txt` | Зависимости для Linux |
| `.env` | Твои ключи (не коммитить!) |
| `.env.example` | Шаблон `.env` |
