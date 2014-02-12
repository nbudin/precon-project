import csv

from django.core.management.base import BaseCommand, CommandError
from precon.models import Slot, Room, Panel, PanelProposal

class Command(BaseCommand):
    args = '<CSVFILE>'
    help = 'Creates the specified schedule from the existing panel proposals'

    def handle(self, *args, **options):
        f = open(args[0], 'rb')
        csvfile = csv.reader(f)

        header = csvfile.next()
        rooms = [Room.objects.get(name=r) for r in header[1:]]

        for row in csvfile:
            print row
            slot = Slot.objects.get(name=row[0])

            for pp_name, room in zip(row[1:], rooms):
                if pp_name:
                    print pp_name
                    pp = PanelProposal.objects.get(name=pp_name)
                    try:
                        Panel.objects.get(name=pp.name)
                    except Panel.DoesNotExist:
                        panel = Panel(name=pp.name, blurb=pp.blurb, type=pp.type, room=room, slot=slot)
                        panel.save()
