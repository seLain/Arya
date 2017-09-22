from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Project, Stage, Task, ActivityLog
from .forms import TaskForm
from .command_bot.bot import Bot

import json

# Create your views here.

@login_required(login_url="/")
def index(request):

	# load all kanban projects
	all_projects = Project.objects.all()

	return render(request, 'kanban/index.html', {'projects': all_projects})

@login_required(login_url="/")
def project_page(request):

	project_id = request.GET.get('id')
	project = Project.objects.get(id=project_id)

	stages = Stage.objects.filter(project=project).order_by('order')
	for stage in stages:
		stage.tasks = Task.objects.filter(project=stage.project, stage=stage)

	recent_activities = ActivityLog.objects.all().order_by('-date')

	return render(request, 'kanban/project.html', 
				  {'project': project, 
				   'stages': stages,
				   'activities': recent_activities})

@login_required(login_url="/")
def task_page(request):

	task_id = request.GET.get('id')
	task = Task.objects.get(id=task_id)

	form = TaskForm(request.POST or None, instance=task)
	if form.is_valid():
		form.save()
		return redirect('/kanban/project?id=%s' % task.project.id)

	return render(request, 'kanban/task.html', {'task': task, 'form': form})

def command(request):

	command = {'text': request.POST['commandText'],
			   'project_id': request.POST['projectID'],
			   'user': request.user}
	# delegate command processing to bot
	bot = Bot()
	responses = bot.take_command(command)

	return HttpResponse(json.dumps(responses), content_type="application/json") 