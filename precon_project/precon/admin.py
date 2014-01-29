from django.contrib import admin

from precon.models import Participant, PanelProposal, PanelProposalResponse, Panel, Panelist

class PanelProposalResponseInline(admin.StackedInline):
    model = PanelProposalResponse
    extra = 0

class ParticipantAdmin(admin.ModelAdmin):
    inlines = [
        PanelProposalResponseInline,
    ]

class PanelistInline(admin.StackedInline):
    model = Panelist
    fields = ['name']

class PanelProposalAdmin(admin.ModelAdmin):
    pass

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(PanelProposal, PanelProposalAdmin)
admin.site.register(PanelProposalResponse)
admin.site.register(Panel)
admin.site.register(Panelist)
