import math
from datetime import datetime, timedelta
from pytz import timezone

class TimeUtil():

  def getHourDiff(self, time):
    datetime_dict = {
        "year": time[0:4],
        "month": time[5:7],
        "day": time[8:10],
        "hour": time[11:13],
        "minute": time[14:16],
    }

    datetime_str = datetime_dict['month'] + '/' + datetime_dict['day'] + '/' + datetime_dict['year'][2:4] + ' ' + datetime_dict['hour'] + ':' + datetime_dict['minute'] + ":00"
    datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    datetime_offset = datetime_object - timedelta(hours=3)

    return math.ceil((datetime.now() - datetime_offset).total_seconds() / 3600)