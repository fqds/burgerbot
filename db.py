# Для запуска без лишних махинаций, бд будет в таком виде

class Messages:
    _messages = []

    def CreateMessage(self, expired_at, manager_id, employee_id, message_text, message_id):
        self._messages.append({
            "expired_at": expired_at,
            "manager_id": int(manager_id),
            "employee_id": int(employee_id),
            "message_text": message_text,
            "message_id": int(message_id),
            "is_answered": False
        })

    def GetMessageByExpiredAt(self, time):
        messages = []
        for i in self._messages:
            print(time, i)
            if i["expired_at"] == time and i["is_answered"] == False:
                messages.append(i)
        return messages

    def GetMessageByMessageID(self, employee_id, message_id):
        for i in self._messages:
            if i["message_id"] == int(message_id) and i["employee_id"] == int(employee_id):
                return i

    def SetInAnsweredTrue(self, employee_id, message_id):
        for i in self._messages:
            if i["message_id"] == int(message_id) and i["employee_id"] == int(employee_id):
                i["is_answered"] = True
                return

DB = Messages()
