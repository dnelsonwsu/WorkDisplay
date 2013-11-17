from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson
from chunks.models import Chunk

import calendar_parse
import os.path, time
import hashlib

ics_path = '/home/py/workspace/calendar_parse/Nelson_Derek_Calendar.ics'

def home(request):

    cal = calendar_parse.ics_calendar()
    schedule = cal.get_todays_schedule(ics_path)
    context = {'schedule': schedule,}
    
    #set the last modified time of the ics file in the cookie
    request.session['last_modified_time'] =  time.ctime(os.path.getmtime(ics_path))
 
    #set a hash of the current tasks in cookie   
    current_tasks_objects = Chunk.objects.filter(key='current_tasks')
   
    current_tasks = ''
    if len(current_tasks_objects) == 1:
        current_tasks = current_tasks_objects[0].content
    
    request.session['current_tasks_hash'] = hashlib.sha1(current_tasks).hexdigest()
    
    return render_to_response('base/index.html', context, context_instance=RequestContext(request))



def ajax_poll(request):
    if request.method == "POST" and request.is_ajax:
        data = {}
        
        last_modified_time = time.ctime(os.path.getmtime(ics_path))
        
        #Check if we need to update the calendar
        if request.session['last_modified_time'] != last_modified_time:
            request.session['last_modified_time'] = last_modified_time
            
            cal = calendar_parse.ics_calendar()
            schedule = cal.get_todays_schedule(ics_path)

            context = {'schedule': schedule,}
            data['calendar_table'] = str(render(request, 'base/calendar.html', context))

        #See if we need to update the current tasks
        current_tasks_objects = Chunk.objects.filter(key='current_tasks')
        if len(current_tasks_objects) == 1:
            current_tasks = current_tasks_objects[0].content
            cur_hash = hashlib.sha1(current_tasks).hexdigest()
            
            if cur_hash != request.session['current_tasks_hash']:
                print "hash diff!!!!!!!"
                
                request.session['current_tasks_hash'] = cur_hash
                data['current_tasks'] = current_tasks        
            
        json = simplejson.dumps(data)
        return HttpResponse(json, mimetype='application/json')
    
        
    else:
        return  HttpResponseServerError("GET petitions are not allowed for this view.")

    


    