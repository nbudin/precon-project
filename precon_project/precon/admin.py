from django.contrib import admin

from precon.models import Participant, PanelProposal, PanelProposalResponse, Panel

class PanelProposalResponseInline(admin.StackedInline):
    model = PanelProposalResponse
    extra = 0

class ParticipantAdmin(admin.ModelAdmin):
    inlines = [
        PanelProposalResponseInline,
    ]

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(PanelProposal)
admin.site.register(PanelProposalResponse)
admin.site.register(Panel)
