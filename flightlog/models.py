from django.db import models
import datetime
import time
from django.utils.timesince import timesince
from datetime import datetime, timedelta

#from datetime import datetime


# Create your models here.

class Aircraft(models.Model):
   MODELS = (('remosGx', 'Remos GX'),
             ('ch60', 'CH 60'))
   REGISTRATIONS = (('hbwyd','HB-WYD'),
                   ('hbwyf','HB-WYF'),
                    ('hbwyg','HB-WYG'),
                    ('hbykm','HB-YKM'))
   model = models.CharField(max_length=10, choices=MODELS)
   registration = models.CharField(max_length=6, choices=REGISTRATIONS)

   def __unicode__(self):
       return self.get_model_display() + " : " + self.get_registration_display()

       
class Pilot(models.Model):
   name = models.CharField(max_length=15)
       
   def __unicode__(self):
       return self.name

       
       
class Flight(models.Model):

  CHOICES = (('select1','select 1'),
	    ('select2','select 2'))
         
  aircraft = models.ForeignKey(Aircraft)
  date = models.DateField()
  fromAirport = models.CharField(max_length=4, verbose_name='from')
  toAirport = models.CharField(max_length=4, verbose_name='to')
  departure_time = models.TimeField()
  arrival_time = models.TimeField()
  pic = models.ForeignKey(Pilot)
  landings = models.PositiveIntegerField()
  night = models.BooleanField(default=False)
  ifr = models.BooleanField(default=False)
  remark = models.TextField()
  #like = models.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

  def flightTime(self):
    start = self.departure_time
    end = self.arrival_time
    startdelta=timedelta(hours=start.hour,minutes=start.minute,seconds=start.second)
    enddelta=timedelta(hours=end.hour,minutes=end.minute,seconds=end.second)

    # deltatime struct
    d =(enddelta-startdelta)

    return int(d.total_seconds())


  def flightTimeFormatted(self):
    total_seconds = self.flightTime()
    hours, remainder = divmod(total_seconds,60*60)
    minutes, seconds = divmod(remainder,60)
     
    return '{}:{}'.format(hours,minutes)
    return '%s:%s:%s' % (d.seconds/60/60, d.seconds/60, d.seconds)



  
  def __unicode__(self):
    return self.fromAirport