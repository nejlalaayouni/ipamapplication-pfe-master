from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Sousreseau
import time
from datetime import datetime

def cron_job(request,id): 
    time.sleep(5)
    Sousreseau.objects.filter(id=id).update(etat=True,derniere_scan=str(datetime.now())) 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))