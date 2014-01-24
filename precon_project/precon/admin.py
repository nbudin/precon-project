from django.contrib import admin

from precon.models import Participant, PanelProposal, ParticipantPanelProposalResponse, Panel

class ParticipantPanelProposalResponseInline(admin.StackedInline):
    model = ParticipantPanelProposalResponse
    extra = 0

class ParticipantAdmin(admin.ModelAdmin):
    inlines = [
        ParticipantPanelProposalResponseInline,
    ]

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(PanelProposal)
admin.site.register(ParticipantPanelProposalResponse)
admin.site.register(Panel)
