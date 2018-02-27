import sys, logging
from importlib import reload
from django.test import TestCase
from kanban.command_bot.bot import PluginsManager

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PluginManagerTest(TestCase):

	def test_load_single_plugin(self):
		reload(sys)
		PluginsManager()._load_plugins('kanban.tests.unit_tests.single_plugin')
		if 'kanban.tests.unit_tests.single_plugin' not in sys.modules:
			raise AssertionError()
		if 'kanban.tests.unit_tests.single_plugin.create_stage' not in sys.modules:
			raise AssertionError()

	def test_load_init_plugins(self):
		reload(sys)
		PluginsManager().init_plugins()
		if 'kanban.command_bot.plugins' not in sys.modules:
			raise AssertionError()

	def test_load_local_plugins(self):
		reload(sys)
		PluginsManager(plugins=['kanban.tests.unit_tests.local_plugins']).init_plugins()
		if 'kanban.tests.unit_tests.local_plugins' not in sys.modules:
			raise AssertionError()
		if 'kanban.tests.unit_tests.local_plugins.create_stage' not in sys.modules:
			raise AssertionError()
		if 'kanban.tests.unit_tests.local_plugins.create_task' not in sys.modules:
			raise AssertionError()

	def test_get_plugins(self):
		reload(sys)
		manager = PluginsManager(plugins=['kanban.tests.unit_tests.single_plugin', 'kanban.tests.unit_tests.local_plugins'])
		manager.init_plugins()
		matched_func_names = set()
		# test: has_matching_plugin
		for func, args in manager.get_plugins('respond_to', 'create stage Test'):
			if func:
				matched_func_names.add(func.__name__)
		if 'create_stage' not in matched_func_names:
			raise AssertionError()
		# test: not has_matching_plugin (there is no such plugin `hallo`)
		reload(sys)
		matched_func_names = set()
		for func, args in manager.get_plugins('respond_to', 'create stage'):
			if func:
				matched_func_names.add(func.__name__)
		if 'create_stage' in matched_func_names:
			raise AssertionError()