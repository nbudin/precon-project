from django.contrib import admin
from django import forms

from precon.models import *

class PanelProposalResponseInline(admin.StackedInline):
    model = PanelProposalResponse
    extra = 0

class PanelProposalResponseTabularInline(admin.TabularInline):
    model = PanelProposalResponse
    extra = 0

class ParticipantAdmin(admin.ModelAdmin):
    inlines = [
        PanelProposalResponseInline,
    ]

class PanelistInline(admin.StackedInline):
    model = Panelist
    fields = ['name']

class PanelProposalInline(admin.StackedInline):
    model = PanelProposal
    fields = ['name']

class PanelProposalForm(forms.ModelForm):
    class Meta:
        model = PanelProposal
        widgets = {
            'panelists': forms.CheckboxSelectMultiple(),
        }

class PanelProposalAdmin(admin.ModelAdmin):
    form = PanelProposalForm
    inlines = [
        PanelProposalResponseTabularInline,
    ]

class PanelistAdmin(admin.ModelAdmin):
    inlines = [
        PanelProposalInline
    ]

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(PanelProposal, PanelProposalAdmin)
admin.site.register(PanelProposalResponse)
admin.site.register(Panelist, PanelistAdmin)
admin.site.register(Schedule)
admin.site.register(Panel)
admin.site.register(Slot)
admin.site.register(Room)
admin.site.register(SiteConfig)
admin.site.register(Day)
admin.site.register(Change)
