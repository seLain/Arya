# -*- coding: utf-8 -*-

import re

from kanban.command_bot.bot import respond_to
from kanban.models import Project, Stage, Task, ActivityLog

@respond_to('move task id=#(.*) to stage (.*)', re.IGNORECASE)
def move_task(command, task_id, stage_name):

	response = {'update': False}

	user = command.body['user']
	project_id = command.body['project_id']
	project = Project.objects.get(id=project_id)
	destination_stage = Stage.objects.get(project=project, title=stage_name)
	task = Task.objects.get(id=task_id)
	if task.stage.title != destination_stage.title and \
		task.stage.project == destination_stage.project:
		task.stage = destination_stage
		task.save()
		log = ActivityLog(actor=user, project=project,
						content=" move task %s to stage %s" % \
						(task.title, destination_stage.title))
		log.save()
		response['update'] = True
		response['stage_title'] = destination_stage.title
		response['task_title'] = task.title
		response['task_id'] = task.id
		response['log'] = str(log)

	return response
