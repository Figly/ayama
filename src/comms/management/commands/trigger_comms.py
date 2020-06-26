import importlib
import logging
import os

from django.core.management.base import BaseCommand

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs a particular communications job, given the args passed."

    def add_arguments(self, parser):
        parser.add_argument("--job", type=str)
        parser.add_argument("--subject", type=str)
        parser.add_argument("--body", type=str)
        parser.add_argument("--to", type=str)
        parser.add_argument("--from", type=str)
        parser.add_argument("--fail_silently", type=bool)

    def handle(self, *args, **kwargs):
        """
        Class method to execute an actual command based on the passed args
        """
        try:
            mod = importlib.import_module(f'comms.jobs.{kwargs["job"]}')
            mod.run(**kwargs)
        except Exception as e:
            log.error(f"Failed to trigger comms. Error: {e}")
            raise e
