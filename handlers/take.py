import re
from telegram import Update
from telegram.ext import ContextTypes
from services.stand_manager import stand_manager
from config.settings import MAX_TASK_LENGTH
from handlers.base import delete_last_message

async def take(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команд /take и /t"""
    chat_id = update.message.chat_id
    user = update.message.from_user.first_name
    args = context.args
    
    if len(args) < 2:
        sent = await update.message.reply_text("Укажи стенд и задачу, например: /take e1 Тест")
        context.chat_data['last_message'] = sent.message_id
        return
    
    match = re.match(r'^(e|a)(\d+)$', args[0], re.IGNORECASE)
    if not match:
        sent = await update.message.reply_text('Неверный формат. Используй "e1" или "a2".')
        context.chat_data['last_message'] = sent.message_id
        return
    
    stand_type, stand_num = match.groups()
    stand_num = int(stand_num)
    
    stand = stand_manager.get_stand(stand_type, stand_num)
    if not stand:
        sent = await update.message.reply_text('Неверный номер стенда.')
        context.chat_data['last_message'] = sent.message_id
        return
    
    task = ' '.join(args[1:])
    if len(task) > MAX_TASK_LENGTH:
        sent = await update.message.reply_text(f'Максимум {MAX_TASK_LENGTH} символов.')
        context.chat_data['last_message'] = sent.message_id
        return
    
    if stand.is_occupied():
        sent = await update.message.reply_text(
            f'Стенд {stand_type}{stand_num} уже занят {stand.user}'
        )
        context.chat_data['last_message'] = sent.message_id
    else:
        stand.occupy(user, task)
        sent = await update.message.reply_text(
            f'{user} занял стенд {stand_type}{stand_num}'
        )
        context.chat_data['last_message'] = sent.message_id