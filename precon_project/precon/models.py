import string, random

from django.db import models
 
def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class Participant(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    modification_time = models.DateTimeField(auto_now=True, editable=False)
    nonce = models.CharField(default=lambda: id_generator(size=6), unique=True, editable=False, max_length=6)

    name = models.CharField("Your name, as you would like it to appear in any published material", max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField("Phone number", max_length=15, null=True, blank=True)
    panel_proposals_responded = models.ManyToManyField('PanelProposal', through='PanelProposalResponse', related_name='participants_responded', null=True, blank=True)
    slots_available = models.ManyToManyField('Slot', related_name='participants_available', null=True, blank=True)
    slots_maybe = models.ManyToManyField('Slot', related_name='participants_maybe', null=True, blank=True)
    anything_else = models.TextField(max_length=1000, null=True, blank=True)

    def responses(self):
        return PanelProposalResponses.objects.filter(participant=self)

    def __unicode__(self):
        return self.name

class Panelist(models.Model):
    name = models.CharField(max_length=50, unique=True)
    participant = models.ForeignKey(Participant, default=None, null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.participant and self.participant.name or self.name


class PanelProposal(models.Model):
    PANEL = 'Panel'
    TALK = 'Talk'
    WORKSHOP = 'Workshop'
    DISCUSSION = 'Discussion'
    TYPE_CHOICES = (
        (PANEL, PANEL),
        (TALK, TALK),
        (WORKSHOP, WORKSHOP),
        (DISCUSSION, DISCUSSION),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=PANEL)
    blurb = models.TextField(max_length=4000)
    needs_panelists = models.BooleanField(default=True)
    panelists = models.ManyToManyField(Panelist, blank=True)

    def responses(self):
        return PanelProposalResponses.objects.filter(panel_proposal=self)

    def __unicode__(self):
        return "%s Proposal: \"%s\"" % (self.type, self.name,)


class PanelProposalResponse(models.Model):
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
    attending_interest = models.CharField("How interested would you be in attending this event?", max_length=50, choices=INTEREST_CHOICES, default=NOT_INTERESTED)
    presenting_interest = models.CharField("How interested would you be in presenting at this event?", max_length=50, choices=INTEREST_CHOICES, default=NOT_INTERESTED)
    presenting_comments = models.TextField(max_length=1000, blank=True)
    attending_comments = models.TextField(max_length=1000, blank=True)

    def __unicode__(self):
        return "Response: \"%s\": %s" % (self.panel_proposal.name, self.participant)


class Panel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    blurb = models.TextField(max_length=4000)
    panelists = models.ManyToManyField(Panelist, blank=True)

    def __unicode__(self):
        return "\"%s\"" % (self.name,)

class Schedule(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

class Slot(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='slots')
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class SiteConfig(models.Model):
    current_schedule = models.ForeignKey(Schedule, default=None, null=True, blank=True, on_delete=models.SET_NULL)
