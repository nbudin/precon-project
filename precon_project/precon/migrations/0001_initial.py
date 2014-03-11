# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table(u'precon_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modification_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('nonce', self.gf('django.db.models.fields.CharField')(default='sc7mha', unique=True, max_length=6)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('anything_else', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('max_panels', self.gf('django.db.models.fields.CharField')(default='0', max_length=10)),
        ))
        db.send_create_signal(u'precon', ['Participant'])

        # Adding M2M table for field slots_attending on 'Participant'
        m2m_table_name = db.shorten_name(u'precon_participant_slots_attending')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm[u'precon.participant'], null=False)),
            ('slot', models.ForeignKey(orm[u'precon.slot'], null=False))
        ))
        db.create_unique(m2m_table_name, ['participant_id', 'slot_id'])

        # Adding M2M table for field slots_available on 'Participant'
        m2m_table_name = db.shorten_name(u'precon_participant_slots_available')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm[u'precon.participant'], null=False)),
            ('slot', models.ForeignKey(orm[u'precon.slot'], null=False))
        ))
        db.create_unique(m2m_table_name, ['participant_id', 'slot_id'])

        # Adding M2M table for field slots_maybe on 'Participant'
        m2m_table_name = db.shorten_name(u'precon_participant_slots_maybe')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm[u'precon.participant'], null=False)),
            ('slot', models.ForeignKey(orm[u'precon.slot'], null=False))
        ))
        db.create_unique(m2m_table_name, ['participant_id', 'slot_id'])

        # Adding model 'Panelist'
        db.create_table(u'precon_panelist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='panelists', on_delete=models.SET_NULL, default=None, to=orm['precon.Participant'], blank=True, null=True)),
        ))
        db.send_create_signal(u'precon', ['Panelist'])

        # Adding model 'PanelProposal'
        db.create_table(u'precon_panelproposal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Panel', max_length=50)),
            ('blurb', self.gf('django.db.models.fields.TextField')(max_length=4000)),
            ('needs_panelists', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('suggested_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='panelproposals_suggested', null=True, to=orm['precon.Panelist'])),
        ))
        db.send_create_signal(u'precon', ['PanelProposal'])

        # Adding M2M table for field panelists on 'PanelProposal'
        m2m_table_name = db.shorten_name(u'precon_panelproposal_panelists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('panelproposal', models.ForeignKey(orm[u'precon.panelproposal'], null=False)),
            ('panelist', models.ForeignKey(orm[u'precon.panelist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['panelproposal_id', 'panelist_id'])

        # Adding model 'PanelProposalResponse'
        db.create_table(u'precon_panelproposalresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modification_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['precon.Participant'])),
            ('panel_proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['precon.PanelProposal'])),
            ('attending_interest', self.gf('django.db.models.fields.CharField')(default='not interested in attending', max_length=50)),
            ('presenting_interest', self.gf('django.db.models.fields.CharField')(default='not interested in presenting', max_length=50)),
            ('presenting_comments', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('attending_comments', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal(u'precon', ['PanelProposalResponse'])

        # Adding model 'Panel'
        db.create_table(u'precon_panel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Panel', max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('blurb', self.gf('django.db.models.fields.TextField')(max_length=4000)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='panels', null=True, to=orm['precon.Room'])),
            ('panel_proposal', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='panels_accepted', null=True, to=orm['precon.PanelProposal'])),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='panels_moderating', null=True, to=orm['precon.Panelist'])),
            ('needs_projector', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'precon', ['Panel'])

        # Adding M2M table for field panelists on 'Panel'
        m2m_table_name = db.shorten_name(u'precon_panel_panelists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('panel', models.ForeignKey(orm[u'precon.panel'], null=False)),
            ('panelist', models.ForeignKey(orm[u'precon.panelist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['panel_id', 'panelist_id'])

        # Adding M2M table for field slot on 'Panel'
        m2m_table_name = db.shorten_name(u'precon_panel_slot')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('panel', models.ForeignKey(orm[u'precon.panel'], null=False)),
            ('slot', models.ForeignKey(orm[u'precon.slot'], null=False))
        ))
        db.create_unique(m2m_table_name, ['panel_id', 'slot_id'])

        # Adding model 'Schedule'
        db.create_table(u'precon_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'precon', ['Schedule'])

        # Adding model 'Day'
        db.create_table(u'precon_day', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'precon', ['Day'])

        # Adding model 'Slot'
        db.create_table(u'precon_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='slots', to=orm['precon.Schedule'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='slots', null=True, to=orm['precon.Day'])),
        ))
        db.send_create_signal(u'precon', ['Slot'])

        # Adding model 'Room'
        db.create_table(u'precon_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rooms', to=orm['precon.Schedule'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'precon', ['Room'])

        # Adding model 'Change'
        db.create_table(u'precon_change', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal(u'precon', ['Change'])

        # Adding model 'SiteConfig'
        db.create_table(u'precon_siteconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_schedule', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['precon.Schedule'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'precon', ['SiteConfig'])


    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table(u'precon_participant')

        # Removing M2M table for field slots_attending on 'Participant'
        db.delete_table(db.shorten_name(u'precon_participant_slots_attending'))

        # Removing M2M table for field slots_available on 'Participant'
        db.delete_table(db.shorten_name(u'precon_participant_slots_available'))

        # Removing M2M table for field slots_maybe on 'Participant'
        db.delete_table(db.shorten_name(u'precon_participant_slots_maybe'))

        # Deleting model 'Panelist'
        db.delete_table(u'precon_panelist')

        # Deleting model 'PanelProposal'
        db.delete_table(u'precon_panelproposal')

        # Removing M2M table for field panelists on 'PanelProposal'
        db.delete_table(db.shorten_name(u'precon_panelproposal_panelists'))

        # Deleting model 'PanelProposalResponse'
        db.delete_table(u'precon_panelproposalresponse')

        # Deleting model 'Panel'
        db.delete_table(u'precon_panel')

        # Removing M2M table for field panelists on 'Panel'
        db.delete_table(db.shorten_name(u'precon_panel_panelists'))

        # Removing M2M table for field slot on 'Panel'
        db.delete_table(db.shorten_name(u'precon_panel_slot'))

        # Deleting model 'Schedule'
        db.delete_table(u'precon_schedule')

        # Deleting model 'Day'
        db.delete_table(u'precon_day')

        # Deleting model 'Slot'
        db.delete_table(u'precon_slot')

        # Deleting model 'Room'
        db.delete_table(u'precon_room')

        # Deleting model 'Change'
        db.delete_table(u'precon_change')

        # Deleting model 'SiteConfig'
        db.delete_table(u'precon_siteconfig')


    models = {
        u'precon.change': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Change'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'precon.day': {
            'Meta': {'object_name': 'Day'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'precon.panel': {
            'Meta': {'ordering': "['name']", 'object_name': 'Panel'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'panels_moderating'", 'null': 'True', 'to': u"orm['precon.Panelist']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'needs_projector': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'panel_proposal': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'panels_accepted'", 'null': 'True', 'to': u"orm['precon.PanelProposal']"}),
            'panelists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'panels'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Panelist']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'panels'", 'null': 'True', 'to': u"orm['precon.Room']"}),
            'slot': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'panels'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Slot']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Panel'", 'max_length': '50'})
        },
        u'precon.panelist': {
            'Meta': {'ordering': "['name']", 'object_name': 'Panelist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'panelists'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['precon.Participant']", 'blank': 'True', 'null': 'True'})
        },
        u'precon.panelproposal': {
            'Meta': {'ordering': "['name']", 'object_name': 'PanelProposal'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'needs_panelists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'panelists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'panelproposals_panelist'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Panelist']"}),
            'suggested_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'panelproposals_suggested'", 'null': 'True', 'to': u"orm['precon.Panelist']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Panel'", 'max_length': '50'})
        },
        u'precon.panelproposalresponse': {
            'Meta': {'object_name': 'PanelProposalResponse'},
            'attending_comments': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'attending_interest': ('django.db.models.fields.CharField', [], {'default': "'not interested in attending'", 'max_length': '50'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'panel_proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.PanelProposal']"}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.Participant']"}),
            'presenting_comments': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'presenting_interest': ('django.db.models.fields.CharField', [], {'default': "'not interested in presenting'", 'max_length': '50'})
        },
        u'precon.participant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Participant'},
            'anything_else': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_panels': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '10'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nonce': ('django.db.models.fields.CharField', [], {'default': "'y8wm3c'", 'unique': 'True', 'max_length': '6'}),
            'panel_proposals_responded': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participants_responded'", 'to': u"orm['precon.PanelProposal']", 'through': u"orm['precon.PanelProposalResponse']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'slots_attending': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'participants_attending'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Slot']"}),
            'slots_available': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'participants_available'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Slot']"}),
            'slots_maybe': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'participants_maybe'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Slot']"})
        },
        u'precon.room': {
            'Meta': {'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rooms'", 'to': u"orm['precon.Schedule']"})
        },
        u'precon.schedule': {
            'Meta': {'object_name': 'Schedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'precon.siteconfig': {
            'Meta': {'object_name': 'SiteConfig'},
            'current_schedule': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['precon.Schedule']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'precon.slot': {
            'Meta': {'object_name': 'Slot'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'slots'", 'null': 'True', 'to': u"orm['precon.Day']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slots'", 'to': u"orm['precon.Schedule']"})
        }
    }

    complete_apps = ['precon']