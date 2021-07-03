from django.http import HttpResponse
from django.urls import reverse 
from django.shortcuts import HttpResponseRedirect

def Index(request):
    # return HttpResponse("I am a homepage")
    return HttpResponseRedirect(reverse('App_Blog:blog_list'))