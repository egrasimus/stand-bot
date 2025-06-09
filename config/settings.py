import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Берем токен из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
STAND_LINKS =  os.getenv('STAND_LINKS')

# Настройки сообщений
MAX_TASK_LENGTH = 20
AUTO_FREE_DAYS = 5