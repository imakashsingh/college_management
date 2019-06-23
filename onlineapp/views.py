from django.shortcuts import render
from django.http import HttpResponse
from onlineapp.models import *
from django.template import loader

# Create your viewss here.

def hello_world(request):
    return HttpResponse("my first response")

#view to get college name
def get_my_college(request):
    val = request.headers["acronym"]
    c = College.objects.filter(acronym = val).values('name')
    #return HttpResponse(c)
    return HttpResponse(c[0]['name'])

#view to get all colleges and their acronyms
def get_all_colleges(request):
    c = College.objects.values('name','acronym')
    result_table = "<table>"
    for i in c:
        result_table+= "<tr>"
        result_table+= "<td>" + i['name'] + "</td>"
        result_table+= "<td>" + i['acronym'] + "</td>"
        result_table+= "</tr>"
    result_table+="</table>"
    return HttpResponse(result_table)

def get_all_colleges_temp(request):
    c = College.objects.values('name','acronym')
    template = loader.get_template('onlineapp/index.html')
    context = {
        'college_list' : c
    }
    return HttpResponse(template.render(context,request))
