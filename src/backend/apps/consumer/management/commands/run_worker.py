from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import autoreload

from apps.consumer.worker import Worker


class Command(BaseCommand):
    help = "Run consumer"  # noqa

    def handle(self, *args, **kwargs):
        if settings.DEBUG:
            autoreload.run_with_reloader(self.run_worker)
        else:
            self.run_worker()

    def run_worker(self):
        self.stdout.write("Running worker...\n")
        worker = Worker()
        worker.run()
