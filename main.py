import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config.settings import TOKEN
from handlers import base, status, take, free, links
from handlers.json_api import get_stands_json, upload_stands_json

def setup_handlers(app: Application):
    # Базовые команды
    app.add_handler(CommandHandler("start", base.start))
    app.add_handler(CommandHandler("help", base.start))
    
    # Основные команды
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("take", take))
    app.add_handler(CommandHandler("free", free))
    app.add_handler(CommandHandler("links", links))
    
    # Короткие алиасы
    app.add_handler(CommandHandler("s", status))
    app.add_handler(CommandHandler("t", take))
    app.add_handler(CommandHandler("f", free))
    app.add_handler(CommandHandler("l", links))

    app.add_handler(CommandHandler("get_json", get_stands_json))
    app.add_handler(CommandHandler("upload_json", upload_stands_json))
    app.add_handler(MessageHandler(filters.Document.FileExtension("json"), upload_stands_json))

def main():
    # Настройка логгирования
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    
    # Настраиваем обработчики
    setup_handlers(app)
    
    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()