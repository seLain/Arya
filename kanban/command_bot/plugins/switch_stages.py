# -*- coding: utf-8 -*-

import re

from kanban.command_bot.bot import respond_to
from kanban.models import Project, Stage, ActivityLog

@respond_to('switch stage (.*) and stage (.*)', re.IGNORECASE)
def switch_stages(command, first_stage_name, second_stage_name):

	response = {'update': False}

	user = command.body['user']
	project_id = command.body['project_id']
	project = Project.objects.get(id=project_id)
	first_stage = Stage.objects.get(project=project_id, title=first_stage_name)
	second_stage = Stage.objects.get(project=project_id, title=second_stage_name)

	# switch order
	largest_order = Stage.objects.filter(project=project).order_by('-order')[0].order
	temp_first_order = first_stage.order
	temp_second_order = second_stage.order
	first_stage.order = largest_order + 1
	first_stage.save()
	second_stage.order = temp_first_order
	second_stage.save()
	first_stage.order = temp_second_order
	first_stage.save()

	log = ActivityLog(actor=user, project=project, \
					content=" switch stage %s and stage %s" % \
					(first_stage.title, second_stage.title))
	log.save()
	response['update'] = True
	response['event'] = 'switch_stage'
	response['first_stage_title'] = first_stage.title
	response['second_stage_title'] = second_stage.title
	response['log'] = str(log)

	return response
