from django.contrib import admin

from flightlog.models import Flight,Aircraft,Pilot

admin.site.register(Pilot)
admin.site.register(Aircraft)
admin.site.register(Flight)
