from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from services.stand_manager import stand_manager
from config.constants import STAND_LINKS
from handlers.base import delete_last_message
import re

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команд /status и /s"""
    chat_id = update.message.chat_id
    await delete_last_message(context, chat_id)
    
    freed = stand_manager.check_and_free_expired()
    current_time = datetime.now()
    
    ecom_status = "<b>ECOM</b>\n"
    admin_status = "<b>Admin</b>\n"
    
    for stand in stand_manager.stands:
        stand_id = f"{stand.type}{stand.number}"
        status_line = f"<a href='{STAND_LINKS[stand_id]}'>Стенд {stand_id}</a>: "
        
        if stand.is_occupied():
            time_diff = current_time - stand.occupied_at
            days_left = 5 - time_diff.days
            hours_left = (timedelta(days=5) - time_diff).seconds // 3600
            
            task = stand.task
            if task and re.match(r'^WEBIM-\d+$', task, re.IGNORECASE):
                task = f'<a href="https://jira.megafon.ru/browse/{task}">{task}</a>'
            
            status_line += (
                f"занят {stand.user} (задача: {task}), "
                f"осталось {days_left}д {hours_left}ч"
            )
        else:
            status_line += "свободен"
        
        if stand.type == 'e':
            ecom_status += status_line + "\n"
        else:
            admin_status += status_line + "\n"
    
    message = f"{ecom_status}\n{admin_status}"
    if freed:
        message += f"\nАвтоматически освобождены: {', '.join(freed)}"
    
    sent = await update.message.reply_text(message, parse_mode="HTML")
    context.chat_data['last_message'] = sent.message_id