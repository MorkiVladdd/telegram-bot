# Telegram бот для приема фотографии и ссылки
# Установка: pip install python-telegram-bot

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ЗАМЕНИТЕ НА ВАШ ТОКЕН ОТ BOTFATHER
TOKEN = "8373173629:AAFLOFDAkjEwTv3vwAOTkn1_cPdB8rU3ujo"

# Хранилище состояния для каждого пользователя
user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    chat_id = update.message.chat_id
    
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Я жду от вас:\n"
        "1. Фотографию 📷\n"
        "2. Ссылку на веб-ресурс 🔗\n\n"
        "Отправьте оба файла, и я вас поблагодарю!"
    )
    
    # Инициализируем данные пользователя
    if chat_id not in user_data:
        user_data[chat_id] = {"photo": False, "link": False}


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик получения фотографии"""
    chat_id = update.message.chat_id
    
    if chat_id not in user_data:
        user_data[chat_id] = {"photo": False, "link": False}
    
    user_data[chat_id]["photo"] = True
    await update.message.reply_text("✅ Спасибо за фотографию!")
    
    # Проверяем оба условия
    await check_completion(update, context, chat_id)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений (ссылок)"""
    chat_id = update.message.chat_id
    message_text = update.message.text
    
    if chat_id not in user_data:
        user_data[chat_id] = {"photo": False, "link": False}
    
    # Проверяем наличие http:// или https://
    if "http://" in message_text or "https://" in message_text:
        user_data[chat_id]["link"] = True
        await update.message.reply_text("✅ Спасибо за ссылку!")
        
        await check_completion(update, context, chat_id)
    else:
        await update.message.reply_text(
            "❌ Пожалуйста, отправьте ссылку содержащую http:// или https://"
        )


async def check_completion(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    """Проверяет выполнены ли оба условия"""
    if user_data[chat_id]["photo"] and user_data[chat_id]["link"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text="🎉 Спасибо за всю информацию! Я получил и фотографию, и ссылку!"
        )
        # Сбрасываем для нового цикла
        user_data[chat_id] = {"photo": False, "link": False}


def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("✅ Бот запущен!")
    application.run_polling()


if __name__ == '__main__':
    main()
