from datetime import datetime

class Log(object):
    def __init__(self,namelog):
       
        self.namelog = namelog
       
    def new_log(self, message):

        self.logs = open(self.namelog,"a")
        now = datetime.now()
        message += "  [{}/{}/{}:{}:{}:{}]\n".format(now.day,now.month,now.year,now.hour,now.minute,now.second)
        self.logs.write(message)
        self.logs.close()