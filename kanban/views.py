from django.shortcuts import render
from django.http import HttpResponse

from .models import Task

# Create your views here.

def index(request):

	# load all kanban tasks
	all_tasks = Task.objects.all()
	data = [task.title for task in all_tasks]
	print(data)

	return render(request, 'kanban/index.html', {'tasks': data})