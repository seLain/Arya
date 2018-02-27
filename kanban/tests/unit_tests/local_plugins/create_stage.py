# -*- coding: utf-8 -*-

import re

from kanban.command_bot.bot import respond_to
from kanban.models import Project, Stage, ActivityLog

@respond_to('create stage (.*)', re.IGNORECASE)
def create_stage(command, stage_name):

	response = {'update': False}

	user = command.body['user']
	project_id = command.body['project_id']
	project = Project.objects.get(id=project_id)
	existed_stages = Stage.objects.filter(project=project)
	largest_order = existed_stages.order_by('-order')[0].order if existed_stages.exists() else 0
	stage, created = Stage.objects.get_or_create(title=stage_name, \
												project=project, \
												order=largest_order+1)
	if created:
		log = ActivityLog(actor=user, project=project, \
						content=" create stage %s" % stage.title)
		log.save()
		response['update'] = True
		response['event'] = 'create_stage'
		response['stage_title'] = stage.title
		response['log'] = str(log)

	return response
