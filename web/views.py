from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

def index(request):
    template = loader.get_template('web/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

@login_required
def sandbox(request):
    template = loader.get_template('web/sandbox.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

@login_required
def dashboard(request):
    template = loader.get_template('web/dashboard.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
