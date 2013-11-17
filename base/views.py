from django.http import HttpResponse
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext
import calendar_parse


def home(request):
    

    cal = calendar_parse.ics_calendar()
    schedule = cal.get_todays_schedule('/home/py/workspace/calendar_parse/Nelson_Derek_Calendar.ics')
      
    context = {'schedule': schedule,}
    
    return render_to_response('base/index.html', context, context_instance=RequestContext(request))
