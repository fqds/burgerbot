from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, CallbackContext
from db import DB

async def _startHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Здравствуйте, {update.message.from_user.first_name}, ваш id:\n{update.message.from_user.id}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text = text)

async def EditMessage(bot_application, chat_id, text, message_id):
    await bot_application.bot.edit_message_text(chat_id=chat_id, text=text, message_id=message_id)

async def SendMessage(bot_application, chat_id, text):
    await bot_application.bot.send_message(chat_id=chat_id, text=text)

async def SendNotification(bot_application, chat_id, text):
    keyboard = [
        [
            InlineKeyboardButton("выполнено", callback_data="task_complited"),
            InlineKeyboardButton("не сделано", callback_data="task_not_complited"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await bot_application.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    return message.message_id

async def _success_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    message = DB.GetMessageByMessageID(chat_id, message_id)
    await query.edit_message_text(
        text=message["message_text"] + "\n\nCOMPLITED"
    )

    manager_text = f"Ha задачу:\n{message['message_text']}, \nБыл получен ответ: 'Выполнено'"
    await SendMessage(context, message["manager_id"], manager_text)
    DB.SetInAnsweredTrue(chat_id, message_id)
    return

async def _fail_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    message = DB.GetMessageByMessageID(query.message.chat.id, query.message.message_id)
    await query.edit_message_text(
        text=message["message_text"] + "\n\nNOT DONE"
    )

    manager_text = f"Ha задачу:\n{message['message_text']}, \nБыл получен ответ: 'He сделано'"
    await SendMessage(context, message["manager_id"], manager_text)
    return

def RunBot(bot_application):
    start_handler = CommandHandler('start', _startHandler)
    success_callback = CallbackQueryHandler(_success_callback, "^task_complited$")
    fail_callback = CallbackQueryHandler(_fail_callback, "^task_not_complited$")
    bot_application.add_handler(success_callback)
    bot_application.add_handler(start_handler)
    bot_application.add_handler(fail_callback)
    bot_application.run_polling()