# -*- coding: utf-8 -*-
import inspect
import os

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Run server tornado web sockets."

    def handle_noargs(self, **options):
    	path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    	path = os.path.dirname(os.path.dirname(path))
    	self.stdout.write('Running server...')
    	os.system("python " + path + "/websockets/server.py")
