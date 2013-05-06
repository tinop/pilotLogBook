# Create your views here.
# Create your views here.
import django.shortcuts
from django.http import HttpResponse
from django.shortcuts import render_to_response
import flightlog.models as M
import utilities
from datetime import date, timedelta, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import pdb;


def sumFlights(flights):
  tot_landings = 0
  tot_flight_time = 0
  pic_flight_time = 0
  dual_flight_time = 0
  
  for flight in flights:
      tot_landings = tot_landings + flight.landings
      tot_flight_time = tot_flight_time + flight.flightTime()
      
  pic = flights.filter(function__iexact='pic')
  for flight in pic:
      pic_flight_time = pic_flight_time + flight.flightTime()
    
  dual = flights.filter(function__iexact='dual')
  for flight in dual:
      dual_flight_time = dual_flight_time + flight.flightTime()

  return (tot_landings, tot_flight_time, pic_flight_time, dual_flight_time)


@login_required
def home(request):
  #return HttpResponse("Hello, world. You're at the poll index.")
  return django.shortcuts.render(request, 'flightlog/index.html')


headers = {'aircraft__model':'des',
  'aircraft__registration':'des',
  'date':'des',
  'fromAirport':'des',
  'toAirport':'des',
  'departure_time':'des',
  'arrival_time':'des',
  'pic':'des',
  'landings':'des',
  'night':'des',
  'ifr':'des',
  'remark':'des',
  'flight_time':'des',}


def toggleSort(sort):
  if headers[sort] == "des":
    headers[sort] = "asc"
  else:
    headers[sort] = "des"  

@login_required
def flightlog(request):
  
  #user = authenticate(username='tino', password='n')
  
  #if user is not None:
    ## the password verified for the user
    #if user.is_active:
      #print("User is valid, active and authenticated")
      #login(request, user)
    #else:
      #print("The password is valid, but the account has been disabled!")
  #else:
    ## the authentication system was unable to verify the username and password
    #print("The username and password were incorrect.")
  
  #user_profile = request.user.get_profile()
  user_profile = request.user.pilotUser
  expireData = user_profile.expireData
  #expireData = date.today()
  print expireData
  
  sort = request.GET.get('sort')
  page = request.GET.get('page')

  if sort is None:
    sort = 'date'
  
  sortBySuffix = '&sort=%s' % sort
  
  flights = M.Flight.objects.filter(user=request.user)

  # if page != None, we are navigating throug pages -> dont toggle the sorting
  if page is None:
    toggleSort(sort) 
  
  if sort == 'flight_time':
      if headers['flight_time'] == "des":
	flights = sorted(flights, key=lambda a: a.flightTime(), reverse=True)
      else:
	flights = sorted(flights, key=lambda a: a.flightTime())
  else:
    
    flights = flights.order_by(sort)
      
    if headers[sort] == "des":
      flights = flights.reverse()
      

  paginator = Paginator(flights, 5)
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
				  'sorted_by_suffix' : sortBySuffix,
				  'displayed_pages' : displayedPages,
				  'flights': flights})

@login_required
def chart(request):
  return django.shortcuts.render(request, 'flightlog/chart.html')

@login_required
def overview(request, year=None):
  
  templateDict = {}
  
  
  #user_profile = request.user.get_profile()
  #expireData = user_profile.expireData
  expireData = date.today()
  d=expireData-timedelta(days=365)
  flights = M.Flight.objects.filter(user=request.user).filter(date__gte=d)
  
  (landings_exp, flight_time_exp, flight_time_pic_exp, flight_time_dual_exp) = sumFlights(flights)
  
  templateDict['expire_date']= expireData
  templateDict['nb_exp'] = len(flights)
  templateDict['landings_exp'] = landings_exp
  templateDict['flight_time_exp'] = utilities.flightTimeFormatted(flight_time_exp)
  templateDict['flight_time_pic_exp'] = utilities.flightTimeFormatted(flight_time_pic_exp)
  templateDict['flight_time_dual_exp'] = utilities.flightTimeFormatted(flight_time_dual_exp)
  
  # all flights
  flights = M.Flight.objects.filter(user=request.user)
  (landings_tot, flight_time_tot, flight_time_pic_tot, flight_time_dual_tot)  = sumFlights(flights)
  
  templateDict['nb_tot'] = len(flights)
  templateDict['landings_tot'] = landings_tot
  templateDict['flight_time_tot'] = utilities.flightTimeFormatted(flight_time_tot)
  templateDict['flight_time_pic_tot'] = utilities.flightTimeFormatted(flight_time_pic_tot)
  templateDict['flight_time_dual_tot'] = utilities.flightTimeFormatted(flight_time_dual_tot)
  
  # last month
  #d=date.today()-timedelta(days=31)
  #flights = M.Flight.objects.filter(date__gte=d)
  #(landings_1m, flight_time_1m) = sumFlights(flights)
  
  # last 3 month
  #d=date.today()-timedelta(days=60)
  #flights = M.Flight.objects.filter(date__gte=d)
  #(landings_3m, flight_time_3m) = sumFlights(flights)
  
  # last year
  if not year:
    year = date.today().year

  
  #flights = M.Flight.objects.filter(date__gte=year)
  flights = M.Flight.objects.filter(user=request.user).filter(date__year = year)
  (landings_y, flight_time_y, flight_time_pic_y, flight_time_dual_y)  = sumFlights(flights)
  #(landings_1y, flight_time_1y) = sumFlights(flights)
  
  templateDict['nb_y'] = len(flights)
  templateDict['landings_y'] = landings_y
  templateDict['flight_time_y'] = utilities.flightTimeFormatted(flight_time_y)
  templateDict['flight_time_pic_y'] = utilities.flightTimeFormatted(flight_time_pic_y)
  templateDict['flight_time_dual_y'] = utilities.flightTimeFormatted(flight_time_dual_y)
  
  firstFlight = M.Flight.objects.filter(user=request.user).order_by('date')[0]

  #templateDict = {'tot_landings': tot_landings,
				  #'tot_flight_time': utilities.flightTimeFormatted(tot_flight_time),
				  #'flight_time_pic': utilities.flightTimeFormatted(flight_time_pic),
				  #'flight_time_dual': utilities.flightTimeFormatted(flight_time_dual),
				  #'landings_exp': landings_exp,
				  #'flight_time_exp': utilities.flightTimeFormatted(flight_time_exp),
				  #'flight_time_pic_exp': utilities.flightTimeFormatted(flight_time_pic_exp),
				  #'flight_time_dual_exp': utilities.flightTimeFormatted(flight_time_dual_exp),
				  #'landings_y': landings_y,
				  #'flight_time_y': utilities.flightTimeFormatted(flight_time_y),
				  #'flight_time_pic_y': utilities.flightTimeFormatted(flight_time_pic_y),
				  #'flight_time_dual_y': utilities.flightTimeFormatted(flight_time_dual_y),
				  #}
  templateDict['current'] = year
  templateDict['range'] = range(firstFlight.date.year, date.today().year+1)
  
  nextYear= M.Flight.objects.filter(date__year = int(year)+1 )
  if nextYear:
    templateDict['nextYear'] = int(year)+1
    
  prevYear= M.Flight.objects.filter(date__year = int(year)-1)
  if prevYear:
    templateDict['prevYear'] = int(year)-1


  
  return django.shortcuts.render(request,'flightlog/overview.html',templateDict)
				  
				  
@login_required  
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


