from django.http import HttpResponse
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext



def parse_ics_calendar(calendar_path):
    pass


def home(request):
    return render_to_response('base/index.html')
