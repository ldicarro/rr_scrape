import math
from datetime import datetime, timedelta
from pytz import timezone

class TimeUtil():
  """
  calculate the time difference between [time] and now.
  converts formatted string to time object

  Parameters
  ----------
  time: string

  Returns
  -------
  number: hours difference
  """
  def getHourDiff(self, time):
    datetime_dict = {
        "year": time[0:4],
        "month": time[5:7],
        "day": time[8:10],
        "hour": time[11:13],
        "minute": time[14:16],
    }

    datetime_object = self.convertStringToTimeObjects(datetime_dict)
    datetime_offset = datetime_object - timedelta(hours=3)

    return math.ceil((datetime.now() - datetime_offset).total_seconds() / 3600)
  
  """
  converts formatted string to time object

  Parameters
  ----------
  dictionary: data and time if this format
  {
        "year",
        "month",
        "day",
        "hour",
        "minute",
    }

  Returns
  -------
  object: datetime object
  """
  def convertStringToTimeObjects(self, datetimeDict):
    datetime_str = datetimeDict['month'] + '/' + datetimeDict['day'] + '/' + datetimeDict['year'][2:4] + ' ' + datetimeDict['hour'] + ':' + datetimeDict['minute'] + ":00"
    return datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')