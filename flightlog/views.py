# Create your views here.
# Create your views here.
import django.shortcuts
from django.http import HttpResponse
import flightlog.models as M

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