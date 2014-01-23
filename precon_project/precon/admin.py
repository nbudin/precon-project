from django.contrib import admin

from precon.models import Participant, PanelProposal, ParticipantPanelProposalResponse

admin.site.register(Participant)
admin.site.register(PanelProposal)
admin.site.register(ParticipantPanelProposalResponse)
