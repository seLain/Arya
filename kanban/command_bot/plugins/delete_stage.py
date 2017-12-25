# -*- coding: utf-8 -*-

import re

from kanban.command_bot.bot import respond_to
from kanban.models import Project, Stage, ActivityLog

@respond_to('delete stage (.*)', re.IGNORECASE)
def delete_stage(command, stage_name):

	response = {'update': False}

	user = command.body['user']
	project_id = command.body['project_id']
	project = Project.objects.get(id=project_id)
	num, dict_del_type_num = Stage.objects.get(title=stage_name, project=project).delete()

	if num > 0:
		log = ActivityLog(actor=user, project=project, 
						  content=" delete stage %s" % stage_name)
		log.save()
		response['update'] = True
		response['event'] = 'delete_stage'
		response['stage_title'] = stage_name
		response['log'] = str(log)

	return response
