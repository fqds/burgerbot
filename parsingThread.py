import time
import datetime
from goolgeSheets import RunTable, ParseSheets
from settings import GMT
from bot import SendNotification

def _toUnixTime(time):
    return (datetime.datetime(int("20" + time[6:8]), int(time[3:5]), int(time[0:2]),  int(time[9:11]) - GMT, int(time[12:14])) - datetime.datetime(1970, 1, 1)).total_seconds()

def _parseData(current_time, sheets_creds):
    new_waiting_answer = [] 
    sheets_info = ParseSheets(sheets_creds)
    for i in sheets_info:
        if current_time == _toUnixTime(i[3]):
            SendNotification()
            new_waiting_answer.append(_toUnixTime(i[3]) + 60, i[0], i[1])

    return new_waiting_answer

def _setNotAnswered(waiting_answer, current_time):
    print(current_time)
    return waiting_answer

def RunParsing(bot_application, waiting_answer):
    sheets_creds = RunTable()
    while True:
        current_time = time.time() // 60 * 60
        waiting_answer = _parseData(current_time, sheets_creds)
        waiting_answer = _setNotAnswered(waiting_answer, current_time)
        time.sleep(60 - time.time() % 60)