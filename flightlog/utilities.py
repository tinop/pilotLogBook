
from datetime import date, timedelta, datetime

   
def flightTimeFormatted(tot_seconds):
   hours, remainder = divmod(tot_seconds,60*60)
   minutes, seconds = divmod(remainder,60)
   
   #return '{}:{}'.format(hours,minutes)
   return '%d:%02d' % (hours, minutes)

