# -*- coding: utf-8 -*-

import re

from ..bot import respond_to
from kanban.models import Project, Stage, Task

@respond_to('delete task id=#(.*)', re.IGNORECASE)
def delete_task(command, task_id):

	response = {'update': False}
	
	task =  Task.objects.get(id=task_id)
	project = task.project
	stage =task.stage
	num, dict_del_type_num = Task.objects.get(id=task_id).delete()

	if num > 0:
		response['update'] = True
		response['event'] = 'delete_task'
		response['stage_title'] = stage.title
		response['task_id'] = task_id

	return response
