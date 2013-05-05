from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from flightlog.models import Flight,Aircraft,Pilot,PilotUser,User

import csv
from django.http import HttpResponse

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
class PilotUserInline(admin.StackedInline):
    model = PilotUser
    can_delete = False
    verbose_name_plural = 'pilot_user'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (PilotUserInline, )

class PilotAdmin(admin.ModelAdmin):
    
    exclude = ('user',)
    list_display = ('name', 'lastName')
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PilotAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Pilot.objects.all()
        return Pilot.objects.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            #usr = UserProfile.objects.get(id=request.user.id)
            obj.user = request.user
        obj.save()


class AircraftAdmin(admin.ModelAdmin):
    
    exclude = ('user',)
    list_display = ('model', 'registration')
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(AircraftAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Aircraft.objects.all()
        return Aircraft.objects.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            #usr = UserProfile.objects.get(id=request.user.id)
            obj.user = request.user
        obj.save()

class PilotUserAdmin(admin.ModelAdmin):

    #exclude = ('user',)
    list_display = ( 'expireData','user')
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PilotUserAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return PilotUser.objects.all()
        return PilotUser.objects.filter(id=request.user)
    
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

    exclude = ('user',)
    list_display = ('aircraft', 'date', 'fromAirport','toAirport','departure_time','arrival_time','operation','pic','landings','night','ifr','function','remark','gpsdata')
    
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(FlightAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Flight.objects.all()
        return Flight.objects.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            #usr = UserProfile.objects.get(id=request.user.id)
            obj.user = request.user
        obj.save()

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(PilotUser, PilotUserAdmin)
admin.site.register(Pilot,PilotAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Aircraft, AircraftAdmin)
