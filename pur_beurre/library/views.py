from django.shortcuts import render

from django.template import loader
from django.http import HttpResponse


def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)
    #template = loader.get_template('library/index.html')
    #return HttpResponse(template.render(request=request))
