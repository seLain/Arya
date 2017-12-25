# -*- coding: utf-8 -*-

import re

from kanban.command_bot.bot import respond_to
from kanban.models import Project, Stage, Task, ActivityLog

@respond_to('delete task id=#(.*)', re.IGNORECASE)
def delete_task(command, task_id):

	response = {'update': False}

	user = command.body['user']
	task =  Task.objects.get(id=task_id)
	task_title = task.title
	project = task.project
	stage =task.stage
	num, dict_del_type_num = Task.objects.get(id=task_id).delete()

	if num > 0:
		log = ActivityLog(actor=user, project=project, 
						  content=" delete task %s" % task_title)
		log.save()
		response['update'] = True
		response['event'] = 'delete_task'
		response['stage_title'] = stage.title
		response['task_id'] = task_id
		response['log'] = str(log)

	return response
