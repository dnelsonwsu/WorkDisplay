from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
import calendar_parse
import os.path, time


ics_path = '/home/py/workspace/calendar_parse/Nelson_Derek_Calendar.ics'

def home(request):
    cal = calendar_parse.ics_calendar()
    schedule = cal.get_todays_schedule(ics_path)
      
    context = {'schedule': schedule,}
    request.session['last_modified_time'] =  time.ctime(os.path.getmtime(ics_path))
    
    return render_to_response('base/index.html', context, context_instance=RequestContext(request))



def calendar_poll(request):
    if request.method == "POST" and request.is_ajax:
        last_modified_time = time.ctime(os.path.getmtime(ics_path))
        
        print "last_modified_time: " + last_modified_time
        print "cookie last_modified_time: " + request.session['last_modified_time']
        
        
        if request.session['last_modified_time'] == last_modified_time:
            return HttpResponse()
        else:
            request.session['last_modified_time']= last_modified_time
            
        cal = calendar_parse.ics_calendar()
        schedule = cal.get_todays_schedule(ics_path)
        context = {'schedule': schedule,}
        return render_to_response('base/calendar.html', context, context_instance=RequestContext(request))
    else:
        return  HttpResponseServerError("GET petitions are not allowed for this view.")

    

    
    
    