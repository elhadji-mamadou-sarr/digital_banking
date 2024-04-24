from django.shortcuts import render
from django.http import JsonResponse
import json

def api_view(request, *args, **kwargs):
 data = {
     'name' : 'sarr',
     'Language' : 'Python',
    }
 
 print(request.body)
 dat = json.loads(request.body)
 print(dat)
 dat['headers'] = dict(request.headers)
 dat['content_type'] = request.content_type
 dat['params'] = dict(request.GET)
 dat['post-data'] = dict(request.POST)
 return JsonResponse(dat)