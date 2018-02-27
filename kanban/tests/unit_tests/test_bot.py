import logging
from django.contrib.auth.models import User
from django.test import TestCase
from kanban.models import Project
from kanban.command_bot.bot import Bot

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BotTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='12345')
		self.project = Project.objects.create(title='TestProj')

	def test_take_command(self):
		bot = Bot()
		command = {'text': 'create stage Test',
					'user': self.user,
					'project_id': self.project.id}
		responses = bot.take_command(command)
		self.assertEqual('create_stage' in responses, True)
		response = responses['create_stage']
		self.assertEqual(response['update'], True)
		self.assertEqual(response['event'], 'create_stage')
		self.assertEqual(response['stage_title'], 'Test')