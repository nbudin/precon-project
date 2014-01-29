from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='precon/home.html')),

    # Examples:
    # url(r'^$', 'precon_project.views.home', name='home'),
    # url(r'^precon_project/', include('precon_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^survey/$', 'precon.views.create_participant', name='create_participant'),
    url(r'^survey/(?P<nonce>[\da-z]+)/$', 'precon.views.record_responses', name='record_responses'),
    url(r'^survey/(?P<nonce>[\da-z]+)/done/$', 'precon.views.survey_done', name='survey_done'),
)
