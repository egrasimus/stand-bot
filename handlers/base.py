from telegram import Update
from telegram.ext import ContextTypes

async def delete_last_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Удаляет последнее сообщение бота в чате"""
    if 'last_message' not in context.chat_data:
        return
        
    try:
        await context.bot.delete_message(
            chat_id=chat_id,
            message_id=context.chat_data['last_message']
        )
    except Exception:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команд /start и /help"""
    help_text = (
        "Привет! Я слежу за тестовыми стендами. Используй команды:\n"
        "/status — показать текущий статус всех стендов\n"
        "/take e<номер> <задача> — занять основной стенд (1-8)\n"
        "/take a<номер> <задача> — занять доп. стенд (1-3)\n"
        "/free e<номер> — освободить основной стенд (1-8)\n"
        "/free a<номер> — освободить доп. стенд (1-3)\n"
        "/links — показать ссылки на все существующие стенды\n"
        "/get_json — получить json данных по тестам\n"
        "/upload_json — загрузить json данных по тестам\n"
        "Стенды освобождаются автоматически через 5 дней."
    )
    
    sent = await update.message.reply_text(help_text)
    context.chat_data['last_message'] = sent.message_id