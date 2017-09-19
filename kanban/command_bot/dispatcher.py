# -*- coding: utf-8 -*-

from __future__ import absolute_import

import importlib, traceback, logging, json, re

logger = logging.getLogger(__name__)

MESSAGE_MATCHER = re.compile(r'^(@.*?\:?)\s(.*)', re.MULTILINE | re.DOTALL)

class CommandDispatcher(object):

    def __init__(self, plugins):
        self._plugins = plugins

    def dispatch_cmd(self, cmd):
        category = 'respond_to'
        text = cmd['text']
        responded = False
        responses = {}

        for func, args in self._plugins.get_plugins(category, text):
            if func:
                responded = True
                try:
                    response = func(Command(cmd), *args)
                    responses[func.__name__] = response
                except Exception as err:
                    logger.exception(err)
                    reply = '[%s] Got problem when handling "%s"\n' % (
                        func.__name__, text)
                    reply += '```\n%s\n```' % traceback.format_exc()

        return responses

class Command(object):

    def __init__(self, body):
        from .bot import PluginsManager
        self._plugins = PluginsManager()
        self._body = body

    @property
    def body(self):
        return self._body
