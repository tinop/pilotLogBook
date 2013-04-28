# Create your views here.
# Create your views here.
import django.shortcuts
from django.http import HttpResponse
from django.shortcuts import render_to_response
import flightlog.models as M
import utilities
from datetime import date, timedelta, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from flightlog.models import Document
from flightlog.forms import DocumentForm


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


headers = {'aircraft__model':'asc',
   'aircraft__registration':'asc',
   'date':'asc',
   'fromAirport':'asc',
   'toAirport':'asc',
   'departure_time':'asc',
   'arrival_time':'asc',
   'pic':'asc',
   'landings':'asc',
   'night':'asc',
   'ifr':'asc',
   'remark':'asc',
   'flight_time':'asc',}


def flightlog(request):
   
   flights = M.Flight.objects.all()
   flights = flights.order_by('-date')
   
   sort = request.GET.get('sort')
   page = request.GET.get('page')
   
   if sort == 'flight_time' and page == None:
      
      if headers['flight_time'] == "des":
         flights = sorted(flights, key=lambda a: a.flightTime(), reverse=True)
         headers['flight_time'] = "asc"
      else:
         headers['flight_time'] = "des"
         flights = sorted(flights, key=lambda a: a.flightTime())
   elif sort is not None and page == None:
         flights = flights.order_by(sort)
         
         if headers[sort] == "des":
            flights = flights.reverse()
            headers[sort] = "asc"
         else:
            headers[sort] = "des"
   
#TODO: the 'sort' is also neede when coiming from the pagination

   paginator = Paginator(flights, 2)
   page = request.GET.get('page')
   try:
      gamesPage = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver the first page
      gamesPage = paginator.page(1)
   except EmptyPage:
      # If page is out of range, deliver the first page
      gamesPage = paginator.page(1) #paginator.num_pages)
   finally:
      HALF_RANGE = 5
      RANGE_SIZE = 2*HALF_RANGE + 1
      minPage = max(1, min(gamesPage.number - HALF_RANGE, paginator.num_pages - RANGE_SIZE + 1))
      maxPage = min(max(gamesPage.number + HALF_RANGE, RANGE_SIZE), paginator.num_pages)
      displayedPages = range(minPage, maxPage+1)

   return django.shortcuts.render(request,
                                  'flightlog/flightlog.html',
                                  {'games_list' : gamesPage,
                                  'players_query_prefix' : 'a',
                                  'page_query_suffix' : 'a',
                                  'ranking_query' : 'a',
                                  'displayed_pages' : displayedPages,
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

def dabs(request):
   filename = 'http://docs.google.com/gview?url=http://www.skyguide.ch/fileadmin/dabs-today/DABS_20130426.pdf&embedded=true'
   when = ''

   if 'when' in request.GET:
      try:
         when = request.GET['when']
         if when == 'Today':
            today = datetime.today()
            datestr = today.strftime('%Y%m%d')
            filename = 'http://docs.google.com/gview?url=http://www.skyguide.ch/fileadmin/dabs-today/DABS_'+ datestr +'.pdf&embedded=true'
         else:
            today = datetime.today() + timedelta(days=1) 
            datestr = today.strftime('%Y%m%d')
            filename = 'http://docs.google.com/gview?url=http://www.skyguide.ch/fileadmin/dabs-tomorrow/DABS_'+ datestr +'.pdf&embedded=true'
         
      except ValueError:
         pass
            

   return django.shortcuts.render(request,
                                  'flightlog/dabs.html',
                                  {'filename' : filename,
                                  'when' : when})

def listd(request):

   # Handle file upload
   if request.method == 'POST':
      form = DocumentForm(request.POST, request.FILES)
      if form.is_valid():
         newdoc = Document(gpsdata = request.FILES['gpsdata'])
         newdoc.save()
         
         # Redirect to the document list after POST
         return HttpResponseRedirect(reverse('flightlog.views.list'))
   else:
      form = DocumentForm() # A empty, unbound form
   
   # Load documents for the list page
   documents = Document.objects.all()
   
   # Render list page with the documents and the form
   return render_to_response(
                             'flightlog/list.html',
                             {'documents': documents, 'form': form},
                             context_instance=RequestContext(request)
                             )


