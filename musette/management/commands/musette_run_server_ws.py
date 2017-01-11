import inspect
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run server tornado web sockets."

    def handle(self, *args, **options):
        self.stdout.write('Running server...')
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe())))
        path = os.path.dirname(os.path.dirname(path))
        self.stdout.write('Tornado server initialized')
        os.system("python " + path + "/websockets/server.py")
