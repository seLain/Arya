from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Project, Task
from .forms import TaskForm

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

def task_page(request):

	task_id = request.GET.get('id')
	task = Task.objects.get(id=task_id)

	form = TaskForm(request.POST or None, instance=task)
	if form.is_valid():
		form.save()
		return redirect('/kanban/project?id=%s' % task.project.id)

	return render(request, 'kanban/task.html', {'task': task, 'form': form})
