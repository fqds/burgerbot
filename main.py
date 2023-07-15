import logging
import threading
from telegram.ext import ApplicationBuilder
from parsingThread import RunParsing
from bot import RunBot
from settings import TG_BOT_TOKEN

logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    waiting_answer = {}
    bot_application = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    parsingThread = threading.Thread(target=RunParsing, args=(bot_application, waiting_answer), name="parsing thread")
    parsingThread.start()
    
    RunBot(bot_application, waiting_answer)