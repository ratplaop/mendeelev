
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

def start_bot():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    
    # Запускаем бота
    updater.start_polling()
    updater.idle()

def start(update, context):
    update.message.reply_text('Добро пожаловать!')

def help(update, context):
    update.message.reply_text('Справка по использованию бота')
