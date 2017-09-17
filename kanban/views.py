from django.shortcuts import render
from django.http import HttpResponse

from .models import Project, Task

# Create your views here.

def index(request):

	# load all kanban projects
	all_projects = Project.objects.all()

	return render(request, 'kanban/index.html', {'projects': all_projects})