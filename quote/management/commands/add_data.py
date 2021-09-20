import random
import sys

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument()

    def handle(self, *args, **kwargs):
        try:

            sys.stdout.write("!SUCCESS!")

        except ():
            raise CommandError('Smth wrong :(')
