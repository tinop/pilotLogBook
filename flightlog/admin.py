from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import django.contrib.staticfiles as STATIC
from flightlog.models import Flight,Aircraft,Pilot,Account,User

import os
import json
import csv
from django.http import HttpResponse

def updateLandingsChart(request):
    flights = Flight.objects.filter(owner=request.user);
    
    landing = dict()
    landing['land'] = []
    for (id, flight) in enumerate(flights, start=1):
        landing['land'].append((id, flight.landings))
    
    filename = None
    if not filename:
        filename = os.path.join(STATIC.utils.settings.STATIC_ROOT, 'chart', 'ranks.json')
#   file = open(filename, 'w')
#   json.dump(landing, file, sort_keys=True, indent=2)
##json.dump(data, file)
#   file.close()

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
        This function returns an export csv action
        'fields' and 'exclude' work like in django ModelForm
        'header' is whether or not to output the column names as the first row
        """
    def export_as_csv(modeladmin, request, queryset):
        """
            Generic csv export admin action.
            based on http://djangosnippets.org/snippets/1697/
            """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
        
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
        
        writer = csv.writer(response)
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode('utf-8') for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'account'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (AccountInline, )

class PilotAdmin(admin.ModelAdmin):
    
    exclude = ('owner',)
    list_display = ('name', 'lastName','owner')
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PilotAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.owner.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Pilot.objects.all()
        return Pilot.objects.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            #usr = UserProfile.objects.get(id=request.user.id)
            obj.owner = request.user
        obj.save()


class AircraftAdmin(admin.ModelAdmin):
    
    exclude = ('owner',)
    list_display = ('registration','model','owner')
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(AircraftAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.owner.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Aircraft.objects.all()
        return Aircraft.objects.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            #usr = UserProfile.objects.get(id=request.user.id)
            obj.owner = request.user
        obj.save()

class AccountAdmin(admin.ModelAdmin):

    #exclude = ('user',)
    list_display = ( 'expireData','user')
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(AccountAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Account.objects.all()
        return Account.objects.filter(id=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            #usr = UserProfile.objects.get(id=request.user.id)
            obj.user = request.user
        obj.save()

class FlightAdmin(admin.ModelAdmin):
    #fields = ['date', 'pic']
    #fieldsets = [
    #                (None,               {'fields': ['night','ifr']}),
    #                ('Date information', {'fields': ['pic', 'aircraft']}),
    #            ]
    actions = [export_as_csv_action("Export selected emails as CSV file", fields=['date','pic','aircraft'], header=False),]

    exclude = ('owner',)
    list_display = ('date', 'departure_time','fromAirport','toAirport')#'departure_time','arrival_time','aircraft','operation','pic','landings','night','ifr','function','remark','gpsdata')
    
    
    #filter the admin dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "aircraft":
            kwargs["queryset"] = Aircraft.objects.filter(owner=request.user)
        if db_field.name == "pic":
            kwargs["queryset"] = Pilot.objects.filter(owner=request.user)
        return super(FlightAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(FlightAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.owner.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Flight.objects.all()
        return Flight.objects.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            #usr = UserProfile.objects.get(id=request.user.id)
            obj.owner = request.user
        obj.save()
        updateLandingsChart(request)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Account)
admin.site.register(Pilot,PilotAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Aircraft, AircraftAdmin)
