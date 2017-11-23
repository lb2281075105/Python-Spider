
#encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from models import MyModel
import json
def index(request):
    content = MyModel.objects.all()
    list = {"content":content}
    return render(request,"myjiekou/index.html",list)

def api(request):
    list = []
    item = {}
    content = MyModel.objects.all()
    for one in content:
        item["name"] = one.name
        item["age"] = one.age
        item["hobby"] = one.hobby
        list.append(item)

    return JsonResponse({"status":200,"date":list})