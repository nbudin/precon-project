from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='precon/home.html'), name='home'),

    # Examples:
    # url(r'^$', 'precon_project.views.home', name='home'),
    # url(r'^precon_project/', include('precon_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^staff/$', 'precon.views.staff_dashboard', name='staff_dashboard'),

    ### survey
    url(r'^survey/$', 'precon.views.create_participant', name='create_participant'),

    # staff survey dashboards
    url(r'^survey/results_dashboard/$', 'precon.views.results_dashboard', name='results_dashboard'),
    url(r'^survey/attending_dashboard/$', 'precon.views.attending_dashboard', name='attending_dashboard'),
    url(r'^survey/presenting_dashboard/$', 'precon.views.presenting_dashboard', name='presenting_dashboard'),
    url(r'^survey/scheduling/$', 'precon.views.scheduling', name='scheduling'),

    # survey itself
    url(r'^survey/(?P<nonce>[\da-z]+)/$', 'precon.views.record_responses', name='record_responses'),
    url(r'^survey/(?P<nonce>[\da-z]+)/done/$', 'precon.views.survey_done', name='survey_done'),

    ### schedule
    url(r'^schedule/$', 'precon.views.schedule', name='schedule'),
    url(r'^schedule/print/$', 'precon.views.schedule_print', name='schedule_print'),
    url(r'^schedule/rooms/print/$', 'precon.views.room_schedule_print', name='room_schedule_print'),
    url(r'^schedule/panels/(?P<nonce>[\da-z]+)/$', 'precon.views.panel_list', name='panel_list'),
    url(r'^schedule/panels/$', 'precon.views.panel_list', name='panel_list'),
    url(r'^schedule/panelists/$', 'precon.views.panelist_list', name='panelist_list'),
    url(r'^schedule/moderators/$', 'precon.views.moderator_list', name='moderator_list'),

)
