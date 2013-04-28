from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'flightlog.views.home', name='home'),
    # url(r'^pilotLogBook/', include('pilotLogBook.foo.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^flightlog.html', 'flightlog.views.flightlog'),
    url(r'^chart.html', 'flightlog.views.chart'),
    url(r'^overview.html', 'flightlog.views.overview'),
    url(r'^dabs.html', 'flightlog.views.dabs'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
