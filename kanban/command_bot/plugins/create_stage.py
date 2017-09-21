# -*- coding: utf-8 -*-

import re

from ..bot import respond_to
from kanban.models import Project, Stage

@respond_to('create stage (.*)', re.IGNORECASE)
def create_stage(command, stage_name):

	response = {'update': False}
	project_id = command.body['project_id']
	project = Project.objects.get(id=project_id)
	largest_order = Stage.objects.filter(project=project).order_by('-order')[0].order
	stage, created = Stage.objects.get_or_create(title=stage_name, 
												 project=project, 
												 order=largest_order+1)
	if created:
		response['update'] = True
		response['event'] = 'create_stage'
		response['stage_title'] = stage.title

	return response
