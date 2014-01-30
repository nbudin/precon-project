from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm, CheckboxSelectMultiple
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from models import Participant, PanelProposal, PanelProposalResponse


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

class FullParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'phone', 'slots_maybe', 'slots_available']
        widgets = {
            'slots_available': CheckboxSelectMultiple(),
            'slots_maybe': CheckboxSelectMultiple(),
        }
    # workaround for https://code.djangoproject.com/ticket/9321
    def __init__(self, *args, **kwargs):
        super(FullParticipantForm, self).__init__(*args, **kwargs)
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

def record_responses(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    if request.method == 'POST':
        participant_form = FullParticipantForm(request.POST, prefix='participant', instance=participant)
        anything_else_form = ParticipantAnythingElseForm(request.POST, prefix='anythingelse', instance=participant)
        pps_forms = build_forms(participant, request.POST)
        if all([f.is_valid() for pp, f in pps_forms]):
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


def survey_done(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    context = { 'participant': participant },
    return render(request, 'precon/survey_done.html', context)
