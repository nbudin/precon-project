from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.forms import ModelForm, CheckboxSelectMultiple
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


from models import Panelist, Participant, PanelProposal, PanelProposalResponse, Slot, Room, Panel, Day, Change


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

class FullParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'phone', 'max_panels', 'slots_attending', 'slots_maybe', 'slots_available',]
        widgets = {
            'slots_attending': CheckboxSelectMultiple(),
            'slots_available': CheckboxSelectMultiple(),
            'slots_maybe': CheckboxSelectMultiple(),
        }
    # workaround for https://code.djangoproject.com/ticket/9321
    def __init__(self, *args, **kwargs):
        super(FullParticipantForm, self).__init__(*args, **kwargs)
        self.fields['slots_attending'].help_text = ''
        self.fields['slots_available'].help_text = ''
        self.fields['slots_maybe'].help_text = ''

class ParticipantAnythingElseForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['anything_else']

class PanelProposalResponseForm(ModelForm):
    class Meta:
        model = PanelProposalResponse
        fields = ['presenting_interest', 'presenting_comments', 'attending_interest', 'attending_comments']

class PanelProposalResponseNoPresentingForm(ModelForm):
    class Meta:
        model = PanelProposalResponse
        fields = ['attending_interest', 'attending_comments']

def panelproposalresponseform_factory(pp, **kwargs):
    if pp.needs_panelists:
        return PanelProposalResponseForm(**kwargs)
    else:
        return PanelProposalResponseNoPresentingForm(**kwargs)

@login_required
def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            return HttpResponseRedirect(reverse('record_responses', kwargs={'nonce': participant.nonce}))
    else:
        form = ParticipantForm()

    context = { 'form': form, }
    return render(request, 'precon/survey_start.html', context)

### NOT A VIEW
def build_forms(participant, post_data=None):
    pfx = lambda pp: "ppr%d" % (pp.id,)

    panel_proposals = PanelProposal.objects.all()
    panel_proposal_response_forms = []
    for pp in panel_proposals:
        try:
            ppr = PanelProposalResponse.objects.get(participant=participant, panel_proposal=pp)
            ppf = panelproposalresponseform_factory(pp, data=post_data, instance=ppr, prefix=pfx(pp))
        except PanelProposalResponse.DoesNotExist:
            ppf = panelproposalresponseform_factory(pp, data=post_data, instance=PanelProposalResponse(), prefix=pfx(pp))

        panel_proposal_response_forms.append( ( pp, ppf ) )

    return panel_proposal_response_forms

@login_required
def record_responses(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    if request.method == 'POST':
        participant_form = FullParticipantForm(request.POST, prefix='participant', instance=participant)
        anything_else_form = ParticipantAnythingElseForm(request.POST, prefix='anythingelse', instance=participant)
        pps_forms = build_forms(participant, request.POST)
        if participant_form.is_valid() and anything_else_form.is_valid() and all([f.is_valid() for pp, f in pps_forms]):
            participant_form.save()
            anything_else_form.save()
            for pp, f in pps_forms:
                ppr = f.save(commit=False)
                ppr.participant = participant
                ppr.panel_proposal = pp
                ppr.save()

            return HttpResponseRedirect(reverse('survey_done', kwargs={'nonce': participant.nonce}))
    else:
        participant_form = FullParticipantForm(prefix='participant', instance=participant)
        anything_else_form = ParticipantAnythingElseForm(prefix='anythingelse', instance=participant)
        pps_forms = build_forms(participant)

    context = {
        'participant': participant,
        'participant_form': participant_form,
        'anything_else_form': anything_else_form,
        'pps_forms': pps_forms,
    }
    return render(request, 'precon/survey.html', context)


@login_required
def survey_done(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    context = { 'participant': participant },
    return render(request, 'precon/survey_done.html', context)

@login_required
def results_dashboard(request):
    ps = Participant.objects.all()

    panelists = Panelist.objects.all()

    pps = list(PanelProposal.objects.all())
    pps.sort(lambda x, y: cmp(x.attending_score(), y.attending_score()), reverse=True)

    most_negative = list(PanelProposal.objects.all())
    most_negative.sort(lambda x, y: cmp(x.negativity(), y.negativity()), reverse=True)

    pprs = PanelProposalResponse.objects.all()

    context = { 
        'participants': ps,
        'panel_proposals': pps,
        'panel_proposal_responses': pprs,
        'most_negative': most_negative,
        'panelists': panelists,
    }

    return render(request, 'precon/results_dashboard.html', context)

@login_required
def attending_dashboard(request):
    slots = Slot.objects.all()

    ps = Participant.objects.all()

    panelists = Panelist.objects.all()

    pps = list(PanelProposal.objects.all())
    pps.sort(lambda x, y: cmp(x.attending_score(), y.attending_score()), reverse=True)

    most_negative = list(PanelProposal.objects.all())
    most_negative.sort(lambda x, y: cmp(x.negativity(), y.negativity()), reverse=True)

    pprs = PanelProposalResponse.objects.all()

    context = { 
        'slots': slots,
        'participants': ps,
        'panel_proposals': pps,
        'panel_proposal_responses': pprs,
        'most_negative': most_negative,
        'panelists': panelists,
    }

    return render(request, 'precon/attending_dashboard.html', context)

@login_required
def scheduling(request):
    slots = Slot.objects.all()
    participants = Participant.objects.all()

    context = {
        'slots': slots,
        'participants': participants,
    }

    return render(request, 'precon/scheduling.html', context)

@login_required
def presenting_dashboard(request):
    slots = Slot.objects.all()

    pps = list(PanelProposal.objects.all())
    pps.sort(lambda x, y: cmp(x.attending_score(), y.attending_score()), reverse=True)

    context = {
        'panel_proposals': pps,
        'slots': slots,
    }

    return render(request, 'precon/presenting_dashboard.html', context)

def schedule(request):
    slots = Slot.objects.all()
    rooms = Room.objects.all()
    days = Day.objects.all()
    changes = Change.objects.all()

    table = zip(days, [ zip(day.slots.all(), [ zip(rooms, [ slot.get_panel_for_room(room) for room in rooms ]) for slot in day.slots.all() ]) for day in days ])

    context = {
        'slots': slots,
        'rooms': rooms,
        'days': days,
        'table': table,
        'changes': changes,
    }

    return render(request, 'precon/schedule.html', context)

def panel_list(request, nonce=None):
    if nonce:
        participant = get_object_or_404(Participant, nonce=nonce)
        panelist = get_object_or_404(Panelist, participant=participant)
        panels = Panel.objects.filter(panelists__in=[panelist])
        if not panels:
            return HttpResponseNotFound()
    else:
        panelist = None
        panels = Panel.objects.all()

    context = {
        'panelist': panelist,
        'panels': panels,
    }

    return render(request, 'precon/panel_list.html', context)

@login_required
def panelist_list(request):
    panelists = Panelist.objects.all()
    slots = Slot.objects.all()

    context = {
        'panelists': panelists,
        'slots': slots,
    }

    return render(request, 'precon/panelist_list.html', context)

@login_required
def moderator_list(request):
    panels = Panel.objects.all()
    panelists = Panelist.objects.all()
    slots = Slot.objects.all()

    context = {
        'panels': panels,
        'panelists': panelists,
        'slots': slots,
    }

    return render(request, 'precon/moderator_list.html', context)


@login_required
def staff_dashboard(request):
    context = {},
    return render(request, 'precon/staff_dashboard.html', context)
