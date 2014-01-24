import string, random

from django.db import models
 
def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class Participant(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    modification_time = models.DateTimeField(auto_now=True, editable=False)
    nonce = models.CharField(default=lambda: id_generator(size=6), unique=True, editable=False, max_length=6)

    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    responses = models.ManyToManyField('PanelProposal', through='ParticipantPanelProposalResponse', blank=True)
    panels = models.ManyToManyField('Panel', related_name='panelists', blank=True)

    def __unicode__(self):
        return self.name


class PanelProposal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    blurb = models.TextField(max_length=4000)

    def __unicode__(self):
        return "Proposal: \"%s\"" % (self.name,)


class ParticipantPanelProposalResponse(models.Model):
    NOT_INTERESTED = 'not interested'
    ACTIVELY_DISINTERESTED = 'actively disinterested'
    POTENTIALLY_INTERESTED = 'potentially interested'
    I_HAVE_TO_BE_THERE = 'I have to be there'
    INTEREST_CHOICES = (
        (NOT_INTERESTED, NOT_INTERESTED),
        (ACTIVELY_DISINTERESTED, ACTIVELY_DISINTERESTED),
        (POTENTIALLY_INTERESTED, POTENTIALLY_INTERESTED),
        (I_HAVE_TO_BE_THERE, I_HAVE_TO_BE_THERE),
    )

    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    modification_time = models.DateTimeField(auto_now=True, editable=False)

    participant = models.ForeignKey(Participant)
    panel_proposal = models.ForeignKey(PanelProposal)
    attending_interest = models.CharField(max_length=50, choices=INTEREST_CHOICES, default=NOT_INTERESTED)
    presenting_interest = models.CharField(max_length=50, choices=INTEREST_CHOICES, default=NOT_INTERESTED)
    comments = models.TextField(max_length=1000, blank=True)

    def __unicode__(self):
        return "%s: %s" % (self.panel_proposal, self.participant)


class Panel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    blurb = models.TextField(max_length=4000)
    # panelists from M2M on Participant

    def __unicode__(self):
        return "\"%s\"" % (self.name,)
