# -*- coding: utf-8 -*-

from __future__ import absolute_import

import imp, importlib, os, re
from glob import glob

from . import settings
from .dispatcher import CommandDispatcher

class Bot(object):
    def __init__(self):
        self._plugins = PluginsManager()
        self._plugins.init_plugins()
        self._dispatcher = CommandDispatcher(self._plugins)

    def take_command(self, command):
        responses = self._dispatcher.dispatch_cmd(command)
        return responses


class PluginsManager(object):
    commands = {
        'respond_to': {},
        'listen_to': {}
    }

    def __init__(self):
        pass

    def init_plugins(self):
        if hasattr(settings, 'PLUGINS'):
            plugins = settings.PLUGINS
        else:
            plugins = ['kanban.command_bot.plugins']

        for plugin in plugins:
            self._load_plugins(plugin)

    @staticmethod
    def _load_plugins(plugin):
        path_name = None
        for mod in plugin.split('.'):
            if path_name is not None:
                path_name = [path_name]
            _, path_name, _ = imp.find_module(mod, path_name)
        for py_file in glob('{}/[!_]*.py'.format(path_name)):
            module = '.'.join((plugin, os.path.split(py_file)[-1][:-3]))
            try:
                _module = importlib.import_module(module)
                if hasattr(_module, 'on_init'):
                    _module.on_init()
            except Exception as err:
                logger.exception(err)

    def get_plugins(self, category, text):
        has_matching_plugin = False
        for matcher in self.commands[category]:
            m = matcher.search(text)
            if m:
                has_matching_plugin = True
                yield self.commands[category][matcher], m.groups()

        if not has_matching_plugin:
            yield None, None


def respond_to(regexp, flags=0):
    def wrapper(func):
        PluginsManager.commands['respond_to'][re.compile(regexp, flags)] = func
        return func

    return wrapper
