# -*- coding: utf-8 -*-

import re

from ..bot import respond_to
from kanban.models import Project, Stage

@respond_to('delete stage (.*)', re.IGNORECASE)
def delete_stage(message, stage_name):

	response = {'update': False}
	project_id = message.body['project_id']
	project = Project.objects.get(id=project_id)
	num, dict_del_type_num = Stage.objects.get(title=stage_name, project=project).delete()

	if num > 0:
		response['update'] = True
		response['event'] = 'delete_stage'
		response['stage_title'] = stage_name

	return response
