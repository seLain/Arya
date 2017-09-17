from django.shortcuts import render
from django.http import HttpResponse

from .models import Project, Task

# Create your views here.

def index(request):

	# load all kanban projects
	all_projects = Project.objects.all()

	return render(request, 'kanban/index.html', {'projects': all_projects})

def project_page(request):

	project_id = request.GET.get('id')
	project = Project.objects.get(id=project_id)

	tasks = Task.objects.filter(project=project)

	return render(request, 'kanban/project.html', {'project': project, 'tasks': tasks})