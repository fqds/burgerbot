import asyncio
import time
import datetime
from db import DB
from goolgeSheets import RunTable, ParseSheets
from settings import GMT
from bot import SendNotification, SendMessage, EditMessage

def _toUnixTime(time):
    try: return (datetime.datetime(int("20" + time[6:8]), int(time[3:5]), int(time[0:2]),  int(time[9:11]) - GMT, int(time[12:14])) - datetime.datetime(1970, 1, 1)).total_seconds()
    except: return None

async def _parseData(bot_application, current_time, sheets_creds):
    sheets_info = ParseSheets(sheets_creds)
    for i in sheets_info:
        if current_time == _toUnixTime(i[3]):
            message_id = await SendNotification(bot_application, i[1], i[2])
            DB.CreateMessage(
                expired_at = _toUnixTime(i[3]) + (int(i[4]) * 60),
                manager_id = i[0],
                employee_id = i[1],
                message_text = i[2],
                message_id = message_id
            )
    return

async def _checkNotAnswered(bot_application, current_time):
    messages = DB.GetMessageByExpiredAt(current_time)
    for i in messages:
        text = f"Ha задачу:\n{i['message_text']}\nнe был получен ответ"
        await SendMessage(bot_application=bot_application, chat_id=i["manager_id"], text=text)
        await EditMessage(bot_application=bot_application, chat_id=i["manager_id"], text=i['message_text'] + "\n\nNOT ANSWERED", message_id=i["message_id"])
    return

def RunParsing(bot_application):
    asyncio.run(_runParsing(bot_application))

async def _runParsing(bot_application):
    sheets_creds = RunTable()
    time.sleep(5) 
    while True:
        current_time = time.time() // 60 * 60
        await _parseData(bot_application, current_time, sheets_creds)
        await _checkNotAnswered(bot_application, current_time)
        time.sleep(60 - time.time() % 60)