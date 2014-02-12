import string, random

from django.db import models
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
 
def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class Participant(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    modification_time = models.DateTimeField(auto_now=True, editable=False)
    nonce = models.CharField(default=lambda: id_generator(size=6), unique=True, editable=False, max_length=6)

    name = models.CharField(max_length=50, help_text="Your name, as you would like it to appear in any published material")
    email = models.EmailField(max_length=50)
    phone = models.CharField("Phone number", max_length=15, null=True, blank=True, help_text="If you're interested in presenting (as a panelist etc.), please give us a phone number so we can reach you during the convention if necessary.")
    panel_proposals_responded = models.ManyToManyField('PanelProposal', through='PanelProposalResponse', related_name='participants_responded', null=True, blank=True)
    slots_attending = models.ManyToManyField('Slot', verbose_name="At which of these times do you expect to be in attendance at Precon?", related_name='participants_attending', null=True, blank=True)
    slots_available = models.ManyToManyField('Slot', verbose_name="At which of these times would you be available AND HAPPY to sit on panels?", related_name='participants_available', null=True, blank=True)
    slots_maybe = models.ManyToManyField('Slot', verbose_name="At which of these times would you be available to sit on panels?", related_name='participants_maybe', null=True, blank=True)
    anything_else = models.TextField("Anything else you'd like to tell us?", max_length=1000, null=True, blank=True)

    MAX_PANELS_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    max_panels = models.CharField("How many panels/other events can we schedule you to present for at MAXIMUM?", max_length=10, choices=MAX_PANELS_CHOICES, default='0')

    def responses(self):
        return PanelProposalResponse.objects.filter(participant=self)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Panelist(models.Model):
    name = models.CharField(max_length=50, unique=True)
    participant = models.ForeignKey(Participant, default=None, null=True, blank=True, related_name='panelists', on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.participant and self.participant.name or self.name

    def name_nbsp(self):
        return mark_safe('&nbsp;'.join(unicode(self).split(' ')))

    class Meta:
        ordering = ['name']


class PanelProposal(models.Model):
    PANEL = 'Panel'
    TALK = 'Talk'
    WORKSHOP = 'Workshop'
    DISCUSSION = 'Discussion'
    TABLETOP = 'Tabletop Game'
    TYPE_CHOICES = (
        (PANEL, PANEL),
        (TALK, TALK),
        (WORKSHOP, WORKSHOP),
        (DISCUSSION, DISCUSSION),
        (TABLETOP, TABLETOP),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=PANEL)
    blurb = models.TextField(max_length=4000)
    needs_panelists = models.BooleanField(default=True)
    panelists = models.ManyToManyField(Panelist, related_name='panelproposals_panelist', null=True, blank=True)
    suggested_by = models.ForeignKey(Panelist, related_name='panelproposals_suggested', null=True, blank=True)

    def responses(self):
        return PanelProposalResponse.objects.filter(panel_proposal=self)

    def attending_score(self):
        rs = self.responses()
        return (rs.attending_definitely_interesteds().count() * 3) + (rs.attending_interesteds().count() * 2) + rs.attending_potentially_interesteds().count()

    def negativity(self):
        return self.responses().attending_actively_disinteresteds().count()

    def __unicode__(self):
        return "%s Proposal: \"%s\"" % (self.type, self.name,)

    class Meta:
        ordering = ['name']

class PanelProposalResponseQuerySet(QuerySet):
    presenting_not_interesteds = lambda x: x.filter(presenting_interest=PanelProposalResponse.PRESENTING_NOT_INTERESTED)
    presenting_all = lambda x: x.exclude(presenting_interest=PanelProposalResponse.PRESENTING_NOT_INTERESTED)
    presenting_if_neededs = lambda x: x.filter(presenting_interest=PanelProposalResponse.PRESENTING_IF_NEEDED)
    presenting_interesteds = lambda x: x.filter(presenting_interest=PanelProposalResponse.PRESENTING_INTERESTED)
    presenting_pick_mes = lambda x: x.filter(presenting_interest=PanelProposalResponse.PRESENTING_PICK_ME)
    presenting_suggesters = lambda x: x.filter(presenting_interest=PanelProposalResponse.PRESENTING_SUGGESTER)

    attending_actively_disinteresteds = lambda x: x.filter(attending_interest=PanelProposalResponse.ATTENDING_ACTIVELY_DISINTERESTED)
    attending_not_interesteds = lambda x: x.filter(attending_interest=PanelProposalResponse.ATTENDING_NOT_INTERESTED)
    attending_potentially_interesteds = lambda x: x.filter(attending_interest=PanelProposalResponse.ATTENDING_POTENTIALLY_INTERESTED)
    attending_interesteds = lambda x: x.filter(attending_interest=PanelProposalResponse.ATTENDING_INTERESTED)
    attending_definitely_interesteds = lambda x: x.filter(attending_interest=PanelProposalResponse.ATTENDING_DEFINITELY_INTERESTED)

class PanelProposalResponseManager(models.Manager):
    def get_query_set(self):
        return PanelProposalResponseQuerySet(self.model)
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)

class PanelProposalResponse(models.Model):
    PRESENTING_NOT_INTERESTED = 'not interested in presenting'
    PRESENTING_IF_NEEDED = 'could be a presenter if needed'
    PRESENTING_INTERESTED = 'would be interested in presenting'
    PRESENTING_PICK_ME = 'would like to present'
    PRESENTING_SUGGESTER = 'I suggested this, and I would like to present'

    PRESENTING_INTEREST_CHOICES = (
        (PRESENTING_NOT_INTERESTED, PRESENTING_NOT_INTERESTED),
        (PRESENTING_IF_NEEDED, PRESENTING_IF_NEEDED),
        (PRESENTING_INTERESTED, PRESENTING_INTERESTED),
        (PRESENTING_PICK_ME, PRESENTING_PICK_ME),
        (PRESENTING_SUGGESTER, PRESENTING_SUGGESTER),
    )

    ATTENDING_ACTIVELY_DISINTERESTED = 'actively disinterested in attending'
    ATTENDING_NOT_INTERESTED = 'not interested in attending'
    ATTENDING_POTENTIALLY_INTERESTED = 'might attend'
    ATTENDING_INTERESTED = 'will likely attend'
    ATTENDING_DEFINITELY_INTERESTED = 'will definitely attend'

    ATTENDING_INTEREST_CHOICES = (
        (ATTENDING_ACTIVELY_DISINTERESTED, ATTENDING_ACTIVELY_DISINTERESTED),
        (ATTENDING_NOT_INTERESTED, ATTENDING_NOT_INTERESTED),
        (ATTENDING_POTENTIALLY_INTERESTED, ATTENDING_POTENTIALLY_INTERESTED),
        (ATTENDING_INTERESTED, ATTENDING_INTERESTED),
        (ATTENDING_DEFINITELY_INTERESTED, ATTENDING_DEFINITELY_INTERESTED),
    )

    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    modification_time = models.DateTimeField(auto_now=True, editable=False)

    participant = models.ForeignKey(Participant)
    panel_proposal = models.ForeignKey(PanelProposal)
    attending_interest = models.CharField("How interested would you be in attending this event?", max_length=50, choices=ATTENDING_INTEREST_CHOICES, default=ATTENDING_NOT_INTERESTED)
    presenting_interest = models.CharField("How interested would you be in presenting at this event?", max_length=50, choices=PRESENTING_INTEREST_CHOICES, default=PRESENTING_NOT_INTERESTED)
    presenting_comments = models.TextField("What (if applicable) makes you interested in presenting at this event?", max_length=1000, null=True, blank=True, help_text="If you suggested this and said so in the field above, you don't need to fill this out.")
    attending_comments = models.TextField("Any comments?", max_length=1000, null=True, blank=True)

    # managers
    objects = PanelProposalResponseManager()

    def __unicode__(self):
        return "Response: \"%s\": %s" % (self.panel_proposal.name, self.participant)


class Panel(models.Model):
    PANEL = 'Panel'
    PANEL_PRESENTER = 'Panelist'
    TALK = 'Talk'
    TALK_PRESENTER = 'Speaker'
    WORKSHOP = 'Workshop'
    WORKSHOP_PRESENTER = 'Leader'
    DISCUSSION = 'Discussion'
    DISCUSSION_PRESENTER = 'Facilitator'
    TABLETOP = 'Tabletop Game'
    TABLETOP_PRESENTER = 'GM'
    
    TYPE_CHOICES = (
        (PANEL, PANEL),
        (TALK, TALK),
        (WORKSHOP, WORKSHOP),
        (DISCUSSION, DISCUSSION),
        (TABLETOP, TABLETOP),
    )

    PRESENTER_TYPES = {
        PANEL: PANEL_PRESENTER,
        TALK: TALK_PRESENTER,
        WORKSHOP: WORKSHOP_PRESENTER,
        DISCUSSION: DISCUSSION_PRESENTER,
        TABLETOP: TABLETOP_PRESENTER,
    }

    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=PANEL)
    name = models.CharField(max_length=100, unique=True)
    blurb = models.TextField(max_length=4000)
    panelists = models.ManyToManyField(Panelist, null=True, blank=True)
    slot = models.ForeignKey('Slot', related_name='panels', null=True, blank=True)
    room = models.ForeignKey('Room', related_name='panels', null=True, blank=True)
    panel_proposal = models.ForeignKey('PanelProposal', related_name='panels_accepted', null=True, blank=True)

    def __unicode__(self):
        return "\"%s\"" % (self.name,)

    def anchor(self):
        return "%d" % (self.id,)

    def panelists_nbsp(self):
        return [panelist.name_nbsp() for panelist in self.panelists.all()]

    def presenter_type(self):
        return self.PRESENTER_TYPES[self.type]

    class Meta:
        ordering = ['name']

class Schedule(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

class Slot(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='slots')
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    def get_panel_for_room(self, room):
        for panel in self.panels.all():
            if panel.room == room:
                return panel

        return None

class Room(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='rooms')
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class SiteConfig(models.Model):
    current_schedule = models.ForeignKey(Schedule, default=None, null=True, blank=True, on_delete=models.SET_NULL)
