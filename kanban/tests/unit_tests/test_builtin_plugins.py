import logging
from django.contrib.auth.models import User
from django.test import TestCase
from kanban.models import Project, Task
from kanban.command_bot.dispatcher import Command
from kanban.command_bot.plugins.create_stage import create_stage
from kanban.command_bot.plugins.create_task import create_task
from kanban.command_bot.plugins.delete_stage import delete_stage
from kanban.command_bot.plugins.delete_task import delete_task
from kanban.command_bot.plugins.move_task import move_task
from kanban.command_bot.plugins.switch_stages import switch_stages

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BuiltInPluginsTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='12345')
		self.project = Project.objects.create(title='TestProj')
		self.task_id = None

	def test_create_stage(self):
		cmd_data = {'text': 'create stage Test',
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = create_stage(command, 'Test')
		self.assertEqual(response['update'], True)
		self.assertEqual(response['event'], 'create_stage')
		self.assertEqual(response['stage_title'], 'Test')

	def test_delete_stage(self):
		self.test_create_stage()
		cmd_data = {'text': 'delete stage Test',
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = delete_stage(command, 'Test')
		self.assertEqual(response['update'], True)
		self.assertEqual(response['event'], 'delete_stage')
		self.assertEqual(response['stage_title'], 'Test')

	def test_create_task(self):
		self.test_create_stage()
		cmd_data = {'text': 'create task Task in stage Test',
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = create_task(command, 'Task', 'Test')
		self.task_id = response['task_id']
		self.assertEqual(response['update'], True)
		self.assertEqual(response['event'], 'create_task')
		self.assertEqual(response['stage_title'], 'Test')
		self.assertEqual(response['task_title'], 'Task')
		self.assertEqual('task_id' in response, True)

	def test_delete_task(self):
		self.test_create_task()
		cmd_data = {'text': 'delete task id=#%s' % str(self.task_id),
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = delete_task(command, self.task_id)
		self.assertEqual(response['update'], True)
		self.assertEqual(response['event'], 'delete_task')
		self.assertEqual(response['stage_title'], 'Test')
		self.assertEqual(response['task_id'], self.task_id)

	def test_move_task(self):
		# create second stage
		cmd_data = {'text': 'create stage Test2',
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = create_stage(command, 'Test2')
		# create and move task
		self.test_create_task()
		cmd_data = {'text': 'move task id=#%s to stage Test2' % str(self.task_id),
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = move_task(command, self.task_id, 'Test2')
		self.assertEqual(response['update'], True)
		self.assertEqual(response['event'], 'move_task')
		self.assertEqual(response['stage_title'], 'Test2')
		self.assertEqual(response['task_title'], 'Task')
		self.assertEqual(response['task_id'], self.task_id)

	def test_switch_stages(self):
		# create first stage
		self.test_create_stage()
		# create second stage
		cmd_data = {'text': 'create stage Test2',
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = create_stage(command, 'Test2')
		# create and move task
		cmd_data = {'text': 'switch stage Test and Test2',
					'user': self.user,
					'project_id': self.project.id}
		command = Command(cmd_data)
		response = switch_stages(command, 'Test', 'Test2')
		self.assertEqual(response['update'], True)
		self.assertEqual(response['event'], 'switch_stages')
		self.assertEqual(response['first_stage_title'], 'Test')
		self.assertEqual(response['second_stage_title'], 'Test2')