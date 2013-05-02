from django.db import models
import datetime
import time
from django.utils.timesince import timesince
from datetime import datetime, timedelta
import utilities
from django.db.models.signals import post_save

#from datetime import datetime

from django.contrib.auth.models import User, UserManager


class Pilot(models.Model):
   name = models.CharField(max_length=15)
   lastName = models.CharField(max_length=15)
   
   def __unicode__(self):
      return self.name[0] + ". " +self.lastName

class UserProfile(models.Model):
   user = models.ForeignKey(User, unique=True)
   #url = models.URLField("Website", blank=True)
   #company = models.CharField(max_length=50, blank=True)
   pilot = models.ForeignKey(Pilot)
   expireData = models.DateField()

   def __unicode__(self):
      return self.pilot.name
      

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



class Flight(models.Model):

   OPERATION = (('se','Single Engine'),
                 ('me','Multiple Engine'))
                 
   FUNCTION = (('pic','PIC'),
                 ('copi','Copi'),
               ('dual','Dual'),
               ('instructor','Instructor'))
   
   aircraft = models.ForeignKey(Aircraft)
   date = models.DateField(default=datetime.now)
   fromAirport = models.CharField(max_length=4, verbose_name='from', default='LSMF')
   toAirport = models.CharField(max_length=4, verbose_name='to', default='LSMF')
   departure_time = models.TimeField()
   arrival_time = models.TimeField()
   operation = models.CharField(max_length=20, choices=OPERATION, default='se')
   pic = models.ForeignKey(Pilot)

   landings = models.PositiveIntegerField(default=1)
   night = models.BooleanField(default=False)
   ifr = models.BooleanField(default=False)
   
   funciton = models.CharField(max_length=20, choices=FUNCTION, default='pic')
   remark = models.TextField(blank=True)
   gpsdata = models.FileField(upload_to='documents/%Y/%m/%d/%H/%M/%S/', blank=True)

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
      return utilities.flightTimeFormatted(self.flightTime())
   
   
   def __unicode__(self):
      return self.date.strftime("%d-%m-%Y ")+self.departure_time.strftime("%H:%M")


class Document(models.Model):
   gpsdata = models.FileField(upload_to='documents/%Y/%m/%d')