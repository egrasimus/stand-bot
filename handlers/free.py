import re
from telegram import Update
from telegram.ext import ContextTypes
from services.stand_manager import stand_manager
from handlers.base import delete_last_message

async def free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команд /free и /f"""
    chat_id = update.message.chat_id
    user = update.message.from_user.first_name
    args = context.args
    
    await delete_last_message(context, chat_id)
    
    if not args:
        sent = await update.message.reply_text('Укажи стенд, например: /free e1')
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
    
    if not stand.is_occupied():
        sent = await update.message.reply_text(f'Стенд {stand_type}{stand_num} уже свободен')
        context.chat_data['last_message'] = sent.message_id
    elif stand.user != user:
        sent = await update.message.reply_text(
            f'Стенд {stand_type}{stand_num} занят {stand.user}. '
            f'Только {stand.user} может его освободить.',
            parse_mode='HTML'
        )
        context.chat_data['last_message'] = sent.message_id
    else:
        stand.free()
        sent = await update.message.reply_text(
            f'{user} освободил стенд {stand_type}{stand_num}'
        )
        context.chat_data['last_message'] = sent.message_id