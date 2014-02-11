# -*- coding: utf-8 -*-

import operator

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from precon.models import Participant, PanelProposal, Panel, Room, Slot

from Numberjack import Matrix, Model, Sum, Gcc, Maximize

SOLVER_NAME = 'Mistral'

def _zero_or_func_factory(func):
    def _ZeroOrFunc(array):
        exprs = []
        for x in xrange(len(array)):
            for y in xrange(x + 1, len(array)):
                exprs.append(array[x] == 0 or array[y] == 0 or func(array[x], array[y]))

        return Sum(exprs) == len(exprs)     # all must be true!

    return _ZeroOrFunc

ZeroOrEq = _zero_or_func_factory(operator.eq)
ZeroOrDiff = _zero_or_func_factory(operator.ne)

#def LogicalIf(p, q):
#    """Returns p -> q."""
#    return not p or q

def LogicalIfAndOnlyIf(p, q):
    """Returns p <-> q."""
    return (not p and not q) or (p and q)

def CountNonZero(array):
    return Sum([array[x] != 0 for x in xrange(len(array))])

def ValueOfZeroOrEqArray(array):
    """Given an array which passes ZeroOrEq, return its numeric value.

    Eg. ValueOfZeroOrEq([0,0,5,5,5,0,0]) == 5
    """
    return Sum(array) / CountNonZero(array)


class Command(BaseCommand):
    args = '<>'
    help = 'Generates a schedule'
    option_list = BaseCommand.option_list + (
        make_option('--optimize',
            action='store_true',
            dest='optimize',
            default=False,
            help='Optimize for happiness'),
        make_option('--commit',
            action='store_true',
            dest='commit',
            default=False,
            help='Write schedule to database'),
        )

    def handle(self, *args, **options):
        participants = Participant.objects.all()
        rooms = Room.objects.all()
        slots = Slot.objects.all()
        panel_proposals = PanelProposal.objects.all()

        # participants := rows
        # room × slot := cols
        # a participant × (room × slot) matrix
        # room(j) = j % rooms.count
        # slot(j) = j / rooms.count
        participants_max = participants.count()
        rooms_max = rooms.count()
        slots_max = slots.count()
        j_max = rooms_max * slots_max
        panel_proposals_max = panel_proposals.count()   # no panel proposal id=0

        print "Participants: %d" % (participants_max,)
        print "Rooms: %d" % (rooms_max,)
        print "Slots: %d" % (slots_max,)
        print "Panel Proposals: %d" % (panel_proposals_max,)

        schedule = Matrix(participants_max, j_max, panel_proposals_max + 1)

        model = Model()

        ### hard constraints
        ## physical constraints

        # don't schedule someone in multiple rooms at once
#        for participant_row in schedule.row:
#            for j_base in xrange(0, j_max, rooms_max):
#                model.add(Sum([participant_row[j_base + r] > 0 for r in xrange(rooms_max)]) <= 1)

        # someone can be on no panels
#        participant_cardinalities = {0: (0, j_max)}
        # someone can't be on any given panel more than once
#        participant_cardinalities.update({k: (0, 1) for k in xrange(1, panel_proposals_max + 1)})
#        for participant_row in schedule.row:
#            model.add(Gcc(participant_row, participant_cardinalities))

        # a room-slot must be wholly given over to a single panel
#        for j_col in schedule.col:
#            model.add(ZeroOrEq(j_col))

        # all room-slots should be zero or different
#        for participant_row in schedule.row:
#            model.add(ZeroOrDiff(participant_row))

        # don't schedule people for times they're not available
#        for participant, participant_row, i in zip(participants, schedule.row, xrange(participants_max)):
#            for slot, j_base in zip(slots, xrange(0, j_max, rooms_max)):
#                if slot not in participant.slots_maybe.all() and slot not in participant.slots_available.all():
#                    model.add([schedule[i, j_base + x] == 0 for x in xrange(rooms_max)])

        # schedule everyone who's currently listed as a panelist on the panels where they're listed

        ## sanity constraints
        # don't schedule more than 5 people per room-slot
#        for j_col in schedule.col:
#            model.add(CountNonZero(j_col) <= 5)

        # EXCEPTIONS TO THE MAX-5-PEOPLE-PER-PANEL RULE

        # don't schedule people for more than their max panels
#        for participant, participant_row in zip(participants, schedule.row):
#            model.add(CountNonZero(participant_row) <= int(participant.max_panels))

        ### soft constraints
#        optimize_exprs = []
        # prefer to schedule panels that people want to attend
#        for j_col in schedule.col:
#            for panel_proposal, pp_number in zip(panel_proposals, xrange(1, panel_proposals_max + 1)):
#                optimize_exprs.append((ValueOfZeroOrEqArray(j_col) == pp_number) * panel_proposal.attending_score())
        
        # prefer to schedule people for panels at times they prefer

        # prefer to schedule panels at times people who want to attend them can make
        # prefer not to schedule people for panels at the same time as panels they want to attend

        if options['optimize']:
            model.add(Maximize(Sum([schedule[i, j] for j in xrange(j_max) for i in xrange(participants_max)])))


        print "Loading %s..." % (SOLVER_NAME,)
        solver = model.load(SOLVER_NAME)
        print "Solving..."
        #solver.setTimeLimit(10)
        soln_p = solver.solveAndRestart()

        print 'Nodes: %d, Time: %.1f' % (solver.getNodes(), solver.getTime())
        if soln_p:
            print schedule

