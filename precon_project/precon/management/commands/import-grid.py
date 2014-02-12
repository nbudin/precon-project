import csv

from django.core.management.base import BaseCommand, CommandError
from precon.models import Slot, Room, Panel, PanelProposal

class Command(BaseCommand):
    args = '<CSVFILE>'
    help = 'Creates the specified schedule from the existing panel proposals'

    def handle(self, *args, **options):
        f = open(args[0], 'rb')
        csvfile = csv.reader(f)

        header = csvfile.readrow()
        rooms = [Room.objects.get(name=r) for r in header[1:]]

        for row in csvfile:
            slot = Slot.objects.get(row[0])

            for pp_name, room in zip(row[1:], rooms):
                pp = PanelProposal.objects.get(name=pp_name)
                panel = Panel(name=pp.name, blurb=pp.blurb, type=pp.type, room=room, slot=slot)
