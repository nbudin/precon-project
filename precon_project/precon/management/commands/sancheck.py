# -*- coding: utf-8 -*-

import sys, csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from precon.models import Participant, PanelProposal, Panel, Room, Slot


class Command(BaseCommand):
    args = '<GRID PANELISTS>'
    help = 'Runs basic sanity-checks against a schedule'
    option_list = BaseCommand.option_list + (
        make_option('--dump-empty',
            action='store_true',
            dest='dump_empty',
            default=False,
            help='Write an empty schedule to STDOUT'),
        )

    def handle(self, *args, **options):
        participants = Participant.objects.all()
        rooms = Room.objects.all()
        slots = Slot.objects.all()
        panel_proposals = PanelProposal.objects.all()

        participants_max = participants.count()
        rooms_max = rooms.count()
        slots_max = slots.count()
        panel_proposals_max = panel_proposals.count()

        print "Participants: %d" % (participants_max,)
        print "Rooms: %d" % (rooms_max,)
        print "Slots: %d" % (slots_max,)
        print "Panel Proposals: %d" % (panel_proposals_max,)
        print

        if options['dump_empty']:
            grid = [['Time'] + [str(r) for r in rooms]]
            for slot in slots:
                grid.append([str(slot)] + ([] * rooms.count()))

            self.stdout.write("GRID.csv:\n")
            grid_writer = csv.writer(self.stdout)
            for grid_row in grid:
                grid_writer.writerow(grid_row)

            self.stdout.write("\n")
            self.stdout.write("PANELISTS.csv:\n")
            for panel_proposal in panel_proposals:
                sys.stdout.write("\"%s\"\n" % (panel_proposal.name,))

            self.stdout.write("\n")
            sys.exit(0)

        grid_f = open(args[0], 'rb')
        grid_csv = csv.reader(grid_f)

        panelists_f = open(args[1], 'rb')
        panelists_csv = csv.reader(panelists_f)

        rooms_txt = grid_csv.readrow()[1:]
        rooms = [Room.objects.get(name=r) for r in rooms_txt]

#        for 


        ### hard constraints
        ## physical constraints
        # don't schedule someone in multiple rooms at once
        # someone can be on no panels
        # someone can't be on any given panel more than once
        # a room-slot must be wholly given over to a single panel
        # all room-slots should be zero or different
        # don't schedule people for times they're not available
        # schedule everyone who's currently listed as a panelist on the panels where they're listed

        ## sanity constraints
        # don't schedule more than 5 people per room-slot
        # EXCEPTIONS TO THE MAX-5-PEOPLE-PER-PANEL RULE
        # don't schedule people for more than their max panels

        ### soft constraints
        # prefer to schedule panels that people want to attend
        # prefer to schedule people for panels at times they prefer
        # prefer to schedule panels at times people who want to attend them can make
        # prefer not to schedule people for panels at the same time as panels they want to attend
