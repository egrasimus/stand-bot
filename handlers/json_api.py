import json
from telegram import Update
from telegram.ext import ContextTypes
from services.stand_manager import stand_manager
from pathlib import Path

async def get_stands_json(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает JSON со всеми стендами"""
    stands_data = []
    for stand in stand_manager.stands:
        stands_data.append({
            'type': stand.type,
            'number': stand.number,
            'user': stand.user,
            'task': stand.task,
            'occupied_at': stand.occupied_at.isoformat() if stand.occupied_at else None,
            'is_occupied': stand.is_occupied()
        })
    
    json_response = json.dumps(stands_data, indent=2, ensure_ascii=False)
    sent = await update.message.reply_text(f"<pre>{json_response}</pre>", parse_mode='HTML')
    context.chat_data['last_message'] = sent.message_id

async def upload_stands_json(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Принимает JSON для обновления данных о стендах"""
    try:
        if not update.message.document:
            sent = await update.message.reply_text("Пожалуйста, отправьте JSON файл")
            context.chat_data['last_message'] = sent.message_id
            return
        
        file = await context.bot.get_file(update.message.document.file_id)
        json_data = await file.download_as_bytearray()
        stands_data = json.loads(json_data.decode('utf-8'))
        
        # Валидация данных
        if not isinstance(stands_data, list):
            raise ValueError("Ожидается массив стендов")
        
        stand_manager.load_from_json(stands_data)
        sent = await update.message.reply_text("Данные успешно обновлены!")
        context.chat_data['last_message'] = sent.message_id
        
    except json.JSONDecodeError:
        sent = await update.message.reply_text("Ошибка: Невалидный JSON файл")
        context.chat_data['last_message'] = sent.message_id
    except Exception as e:
        sent = await update.message.reply_text(f"Ошибка: {str(e)}")
        context.chat_data['last_message'] = sent.message_id