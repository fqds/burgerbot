from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def _startHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Здравствуйте, {update.message.from_user.first_name}, ваш id:\n{update.message.from_user.id}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text = text)

async def SendMessage(chat_id, text):
    pass

async def SendNotification(chat_id, text):
    await SendMessage(chat_id, text)

def RunBot(bot_application, waiting_answer):
    start_handler = CommandHandler('start', _startHandler)
    bot_application.add_handler(start_handler)
    bot_application.run_polling()