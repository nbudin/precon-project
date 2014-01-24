from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.forms.formsets import formset_factory, inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from models import Participant, PanelProposal, ParticipantPanelProposalResponse


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        exclude = ['panels', 'responses']

class ParticipantPanelProposalResponseForm(ModelForm):
    class Meta:
        model = ParticipantPanelProposalResponse
        exclude = ['participant']

ParticipantPanelProposalResponseFormset = inlineformset_factory(Participant, ParticipantPanelProposalResponse, extra=0)


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


def record_responses(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    if request.method == 'POST':
        formset = ParticipantPanelProposalResponseFormset(request.POST, instance=participant)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('survey_done', kwargs={'nonce': participant.nonce}))
    else:
        formset = ParticipantPanelProposalResponseFormset(instance=participant)

    context = { 'participant': participant, 'formset': formset, }
    return render(request, 'precon/survey.html', context)


def survey_done(request, nonce):
    participant = get_object_or_404(Participant, nonce=nonce)

    context = { 'participant': participant },
    return render(request, 'precon/survey_done.html', context)
