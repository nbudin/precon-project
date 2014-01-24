from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from models import Participant, PanelProposal, PanelProposalResponse


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        exclude = ['panels', 'responses']

class PanelProposalResponseForm(ModelForm):
    class Meta:
        model = PanelProposalResponse
        exclude = ['participant', 'panel_proposal']


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
            panel_proposal_response_forms.append( ( pp, PanelProposalResponseForm(data=post_data, instance=ppr, prefix=pfx(pp)) ) )
        except PanelProposalResponse.DoesNotExist:
            panel_proposal_response_forms.append( ( pp, PanelProposalResponseForm(data=post_data, instance=PanelProposalResponse(), prefix=pfx(pp)) ) )
    return panel_proposal_response_forms

def record_responses(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    if request.method == 'POST':
        pps_forms = build_forms(participant, request.POST)
        if all([f.is_valid() for pp, f in pps_forms]):
            for pp, f in pps_forms:
                ppr = f.save(commit=False)
                ppr.participant = participant
                ppr.panel_proposal = pp
                ppr.save()

            return HttpResponseRedirect(reverse('survey_done', kwargs={'nonce': participant.nonce}))
    else:
        pps_forms = build_forms(participant)

    context = { 'participant': participant, 'pps_forms': pps_forms, }
    return render(request, 'precon/survey.html', context)


def survey_done(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    context = { 'participant': participant },
    return render(request, 'precon/survey_done.html', context)
