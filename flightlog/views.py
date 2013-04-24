# Create your views here.
# Create your views here.
import django.shortcuts
from django.http import HttpResponse
import flightlog.models as M
import utilities
from datetime import date, timedelta


def sumFlights(flights):
   tot_landings = 0
   tot_flight_time = 0
   
   for flight in flights:
      tot_landings = tot_landings + flight.landings
      tot_flight_time = tot_flight_time + flight.flightTime()

   return (tot_landings, tot_flight_time)



def home(request):
   #return HttpResponse("Hello, world. You're at the poll index.")
   return django.shortcuts.render(request, 'flightlog/index.html')


def flightlog(request):
   flights = M.Flight.objects.all()
   return django.shortcuts.render(request,
                                  'flightlog/flightlog.html',
                                  {'games_list' : 'a',
                                  'players_query_prefix' : 'a',
                                  'page_query_suffix' : 'a',
                                  'ranking_query' : 'a',
                                  'displayed_pages' : 'a',
                                  'date_title' : 'a',
                                  'opponents_title' : 'a',
                                  'flights': flights})


def chart(request):
   return django.shortcuts.render(request, 'flightlog/chart.html')

def overview(request):
   
   # all flights
   flights = M.Flight.objects.all()
   (tot_landings, tot_flight_time) = sumFlights(flights)
   
   # last month
   d=date.today()-timedelta(days=31)
   flights = M.Flight.objects.filter(date__gte=d)
   (landings_1m, flight_time_1m) = sumFlights(flights)
   
   # last 3 month
   d=date.today()-timedelta(days=60)
   flights = M.Flight.objects.filter(date__gte=d)
   (landings_3m, flight_time_3m) = sumFlights(flights)
   
   # last year
   d=date.today()-timedelta(days=365)
   flights = M.Flight.objects.filter(date__gte=d)
   (landings_1y, flight_time_1y) = sumFlights(flights)
   
   return django.shortcuts.render(request,
                                  'flightlog/overview.html',
                                  {'tot_landings': tot_landings,
                                   'tot_flight_time': utilities.flightTimeFormatted(tot_flight_time),
                                   'landings_1m': landings_1m,
                                   'flight_time_1m': utilities.flightTimeFormatted(flight_time_1m),
                                   'landings_3m': landings_3m,
                                   'flight_time_3m': utilities.flightTimeFormatted(flight_time_3m),
                                   'landings_1y': landings_1y,
                                   'flight_time_1y': utilities.flightTimeFormatted(flight_time_1y)
                                  })




