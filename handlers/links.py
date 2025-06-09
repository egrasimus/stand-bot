from telegram import Update
from telegram.ext import ContextTypes
from config.settings import STAND_LINKS
from handlers.base import delete_last_message

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команд /links и /l"""
    chat_id = update.message.chat_id
    await delete_last_message(context, chat_id)
    
    ecom_links = "<b>ECOM:</b>\n"
    admin_links = "<b>Admin:</b>\n"
    
    for stand_id, url in STAND_LINKS.items():
        link_line = f'<a href="{url}">Стенд {stand_id}: {url}</a>'
        
        if stand_id.startswith('e'):
            ecom_links += link_line + "\n"
        else:
            admin_links += link_line + "\n"
    
    message = "<b>Ссылки на стенды</b>\n\n" + ecom_links + "\n" + admin_links
    sent = await update.message.reply_text(
        message,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    context.chat_data['last_message'] = sent.message_id