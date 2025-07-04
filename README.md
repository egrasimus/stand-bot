# Stand-Bot 🤖

Телеграм-бот для управления стендами (тестовыми средами) с автоматическим освобождением и JSON-импортом/экспортом.

## 📌 Возможности

- Просмотр статуса всех стендов (`/status`)
- Занятие стенда (`/take <тип><номер> <задача>`)  
- Освобождение стенда (`/free <тип><номер>`)  
- Автоматическое освобождение через `AUTO_FREE_DAYS` дней  
- Короткие команды: `/s`, `/t`, `/f`  
- Экспорт/импорт состояния в JSON  
- Быстрые ссылки на стенды (`/links`)  

## 🛠 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/egrasimus/stand-bot.git
   cd stand-bot
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Настройте конфигурацию в `.env`:
   ```python
    TELEGRAM_BOT_TOKEN=<Ваш Токен>
    STAND_LINKS='{
    "e1": "https://example/",
    "e2": "https://example/",
    ...
    }'
   ```

4. Запустите бота:
   ```bash
   python main.py
   ```

## 🎮 Использование

### Основные команды
| Команда | Описание | Пример |
|---------|----------|--------|
| `/start` | Приветствие | |
| `/status` (`/s`) | Статус стендов | |
| `/take <тип><номер> <задача>` (`/t`) | Занять стенд | `/take e5 API-тесты` |
| `/free <тип><номер>` (`/f`) | Освободить стенд | `/free a2` |
| `/links` (`/l`) | Ссылки на стенды | |

### JSON-экспорт/импорт
- `/get_json` — скачать текущее состояние  
- `/upload_json` + файл — загрузить состояние  

## 🌍 Пример JSON
```json
[
  {"type": "e", "number": 1, "user": "ivan", "task": "Тесты UI", "occupied_at": "2023-10-20T12:00:00"},
  {"type": "a", "number": 2, "user": null, "task": null, "occupied_at": null}
]
```

## 🔄 Автоосвобождение
Бот автоматически освобождает стенды, занятые дольше `AUTO_FREE_DAYS` дней (настраивается в `config/settings.py`).

## 📜 Лицензия
MIT
