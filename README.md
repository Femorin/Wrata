# Wrata — скриншот → ИИ → Telegram

WRATA - СПИШИ АБСОЛЮТНО ВСЕ!
Нажми горячую клавишу — скриншот уйдёт в нейросеть Pixtral (Mistral AI), она ответит на вопрос с экрана и пришлёт ответ в Telegram.

---

## Установка

**1. Установи зависимости**

```
pip install keyboard mss Pillow requests mistralai python-dotenv
```

**2. Создай `.env` файл**

Скопируй `.env.example` → `.env` и заполни своими ключами:

```
cp .env.example .env
```

**3. Запусти**

Через консоль:
```
python screen_tg.py
```

Или двойным кликом по `start.vbs` — запускает без окна консоли (рекомендуется).

Программа запустится **полностью невидимо** — без иконки в трее, без окна, без консоли.
В Task Manager будет виден только стандартный процесс `pythonw.exe`.

**Закрыть программу:** нажми `Ctrl + Alt + Shift + Q` (можно сменить в `.env` через `QUIT_HOTKEY`).
Или открой Task Manager → найди `pythonw.exe` → завершить процесс.

---

## Где брать ключи

### Telegram Bot Token (`BOT_TOKEN`)

1. Открой Telegram, найди [@BotFather](https://t.me/BotFather)
2. Отправь `/newbot`
3. Придумай имя и юзернейм для бота
4. BotFather пришлёт токен вида `1234567890:AAH...` — скопируй его в `BOT_TOKEN`

### Telegram Chat ID (`CHAT_ID`)

1. Напиши что-нибудь своему боту
2. Открой [@userinfobot](https://t.me/userinfobot) и нажми `/start`
3. Он покажет твой ID — скопируй в `CHAT_ID`

### Mistral API Key (`MISTRAL_API_KEY`)

1. Зайди на [console.mistral.ai](https://console.mistral.ai)
2. Зарегистрируйся
3. Перейди в раздел **API Keys** → **Create new key**
4. Скопируй ключ в `MISTRAL_API_KEY`

> Бесплатный тир доступен без привязки карты, есть лимиты по запросам в минуту.

---

## Горячие клавиши

В файле `.env` настраиваются две клавиши:

| Переменная | По умолчанию | Действие |
|------------|-------------|---------|
| `HOTKEY` | `f8` | Сделать скриншот и отправить в ИИ |
| `QUIT_HOTKEY` | `ctrl+alt+shift+q` | Завершить программу |

### Настройка `HOTKEY`

В файле `.env` измени значение `HOTKEY` на нужную клавишу.

### Функциональные клавиши
| Значение | Клавиша |
|----------|---------|
| `f1` | F1 |
| `f2` | F2 |
| `f3` | F3 |
| `f4` | F4 |
| `f5` | F5 |
| `f6` | F6 |
| `f7` | F7 |
| `f8` | F8 (по умолчанию) |
| `f9` | F9 |
| `f10` | F10 |
| `f11` | F11 |
| `f12` | F12 |

### Буквы
| Значение | Клавиша |
|----------|---------|
| `a` … `z` | A … Z |

### Цифры (основной ряд)
| Значение | Клавиша |
|----------|---------|
| `0` … `9` | 0 … 9 |

### Цифровой блок (Numpad)
| Значение | Клавиша |
|----------|---------|
| `num 0` … `num 9` | Numpad 0 … 9 |
| `num +` | Numpad + |
| `num -` | Numpad - |
| `num *` | Numpad * |
| `num /` | Numpad / |
| `num enter` | Numpad Enter |
| `num .` | Numpad . |

### Навигация
| Значение | Клавиша |
|----------|---------|
| `up` | Стрелка вверх |
| `down` | Стрелка вниз |
| `left` | Стрелка влево |
| `right` | Стрелка вправо |
| `home` | Home |
| `end` | End |
| `page up` | Page Up |
| `page down` | Page Down |
| `insert` | Insert |
| `delete` | Delete |

### Системные
| Значение | Клавиша |
|----------|---------|
| `enter` | Enter |
| `space` | Пробел |
| `backspace` | Backspace |
| `tab` | Tab |
| `escape` | Escape |
| `caps lock` | Caps Lock |
| `num lock` | Num Lock |
| `scroll lock` | Scroll Lock |
| `pause` | Pause / Break |
| `print screen` | Print Screen |

### Модификаторы (только как часть комбинации)
| Значение | Клавиша |
|----------|---------|
| `ctrl` | Ctrl |
| `shift` | Shift |
| `alt` | Alt |
| `windows` | Win |

### Примеры комбинаций
```
HOTKEY=ctrl+shift+s
HOTKEY=alt+f9
HOTKEY=ctrl+alt+p
```

---

## Файлы

| Файл | Описание |
|------|----------|
| `screen_tg.py` | Основной скрипт |
| `start.vbs` | Запуск без окна консоли (двойной клик) |
| `.env` | Твои секретные ключи (не коммитить!) |
| `.env.example` | Шаблон для других пользователей |
| `.gitignore` | Исключает `.env` из git |
