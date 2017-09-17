from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth

def index(request):

    if login(request):
        return HttpResponseRedirect('/kanban/')
    else:
        return render(request, 'index.html', locals())

def login(request):

    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return True
    else:
        if username != "" or password !="":
          return False

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')