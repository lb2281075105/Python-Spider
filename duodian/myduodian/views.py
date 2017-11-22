from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from myduodian.models import *
def index(request):
    context = {"list":AiDuoDian.objects.all()}
    return render(request,'myduodian/index.html',context)