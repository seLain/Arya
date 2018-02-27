# -*- coding: utf-8 -*-

import re

from kanban.command_bot.bot import respond_to
from kanban.models import Project, Stage, Task, ActivityLog

@respond_to('create task (.*) in stage (.*)', re.IGNORECASE)
def create_task(command, task_name, stage_name):

	response = {'update': False}

	user = command.body['user']
	project_id = command.body['project_id']
	project = Project.objects.get(id=project_id)
	stage = Stage.objects.get(project=project, title=stage_name)
	task, created = Task.objects.get_or_create(title=task_name, \
											project=project, \
											stage=stage, \
											creator=user)
	if created:
		log = ActivityLog(actor=user, project=project, \
						content=" create task %s in stage %s" % \
						(task.title, stage.title))
		log.save()
		response['update'] = True
		response['event'] = 'create_task'
		response['stage_title'] = stage.title
		response['task_title'] = task.title
		response['task_id'] = task.id
		response['log'] = str(log)

	return response
