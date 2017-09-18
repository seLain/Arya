from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Project, Stage, Task
from .forms import TaskForm

import json

# Create your views here.

def index(request):

	# load all kanban projects
	all_projects = Project.objects.all()

	return render(request, 'kanban/index.html', {'projects': all_projects})

def project_page(request):

	project_id = request.GET.get('id')
	project = Project.objects.get(id=project_id)

	stages = Stage.objects.filter(project=project).order_by('order')
	for stage in stages:
		stage.tasks = Task.objects.filter(project=stage.project, stage=stage)

	return render(request, 'kanban/project.html', 
				  {'project': project, 'stages': stages})

def task_page(request):

	task_id = request.GET.get('id')
	task = Task.objects.get(id=task_id)

	form = TaskForm(request.POST or None, instance=task)
	if form.is_valid():
		form.save()
		return redirect('/kanban/project?id=%s' % task.project.id)

	return render(request, 'kanban/task.html', {'task': task, 'form': form})

def command(request):

	command_text = request.POST['commandText']
	# [ToDo] apply command dispatch pattern to deal with this part
	response = command_dispatch(command_text, request.POST)

	return HttpResponse(json.dumps(response), content_type="application/json") 

def command_dispatch(command_text, request_post):

	# [ToDo] using CLI command processing library to deal with this part
	command_text = command_text.strip()
	command_args = [arg for arg in command_text.split(' ') if arg != ' ']

	response = {'update': False}
	if len(command_args) == 3 :
		if command_args[0].lower() == 'create' and command_args[1].lower() == 'stage':
			project = Project.objects.get(id=request_post['projectID'])
			largest_order = Stage.objects.filter(project=project).order_by('-order')[0].order
			stage, created = Stage.objects.get_or_create(title=command_args[2], 
														 project=project, 
														 order=largest_order+1)
			if created:
				response['update'] = True
				response['stage_title'] = stage.title

	return response