import csv

from django.core.management.base import BaseCommand, CommandError
from precon.models import Panel, Panelist, Participant

class Command(BaseCommand):
    args = '<CSVFILE>'
    help = 'Adds panelists to panels'

    def handle(self, *args, **options):
        f = open(args[0], 'rb')
        csvfile = csv.reader(f)

        header = csvfile.next() # throw away first line

        for row in csvfile:
            panel_name = row[0]
            if panel_name:
                print "Panel: %s" % (panel_name,)
                panel = Panel.objects.get(name=panel_name)

                for panelist_name in row[1:]:
                    if panelist_name:
                        print panelist_name
                        try:
                            panelist = Panelist.objects.get(name=panelist_name)
                        except Panelist.DoesNotExist:
                            participant = Participant.objects.get(name=panelist_name)
                            panelist = Panelist(name=participant.name, participant=participant)
                            panelist.save()

                        panel.panelists.add(panelist)
                        panel.save()
