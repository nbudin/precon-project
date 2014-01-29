# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Schedule'
        db.create_table(u'precon_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'precon', ['Schedule'])

        # Adding model 'SiteConfig'
        db.create_table(u'precon_siteconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_schedule', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['precon.Schedule'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'precon', ['SiteConfig'])

        # Adding model 'Slot'
        db.create_table(u'precon_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='slots', to=orm['precon.Schedule'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'precon', ['Slot'])

        # Adding field 'Participant.phone'
        db.add_column(u'precon_participant', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Participant.anything_else'
        db.add_column(u'precon_participant', 'anything_else',
                      self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True),
                      keep_default=False)

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


    def backwards(self, orm):
        # Deleting model 'Schedule'
        db.delete_table(u'precon_schedule')

        # Deleting model 'SiteConfig'
        db.delete_table(u'precon_siteconfig')

        # Deleting model 'Slot'
        db.delete_table(u'precon_slot')

        # Deleting field 'Participant.phone'
        db.delete_column(u'precon_participant', 'phone')

        # Deleting field 'Participant.anything_else'
        db.delete_column(u'precon_participant', 'anything_else')

        # Removing M2M table for field slots_available on 'Participant'
        db.delete_table(db.shorten_name(u'precon_participant_slots_available'))

        # Removing M2M table for field slots_maybe on 'Participant'
        db.delete_table(db.shorten_name(u'precon_participant_slots_maybe'))


    models = {
        u'precon.panel': {
            'Meta': {'object_name': 'Panel'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'panelists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['precon.Panelist']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'precon.panelist': {
            'Meta': {'object_name': 'Panelist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['precon.Participant']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'precon.panelproposal': {
            'Meta': {'object_name': 'PanelProposal'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'needs_panelists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'panelists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['precon.Panelist']", 'symmetrical': 'False', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Panel'", 'max_length': '50'})
        },
        u'precon.panelproposalresponse': {
            'Meta': {'object_name': 'PanelProposalResponse'},
            'attending_interest': ('django.db.models.fields.CharField', [], {'default': "'not interested'", 'max_length': '50'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'panel_proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.PanelProposal']"}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.Participant']"}),
            'presenting_interest': ('django.db.models.fields.CharField', [], {'default': "'not interested'", 'max_length': '50'})
        },
        u'precon.participant': {
            'Meta': {'object_name': 'Participant'},
            'anything_else': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'nonce': ('django.db.models.fields.CharField', [], {'default': "'ut2q4t'", 'unique': 'True', 'max_length': '6'}),
            'panel_proposals_responded': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'participants_responded'", 'to': u"orm['precon.PanelProposal']", 'through': u"orm['precon.PanelProposalResponse']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'slots_available': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'participants_available'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Slot']"}),
            'slots_maybe': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'participants_maybe'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Slot']"})
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slots'", 'to': u"orm['precon.Schedule']"})
        }
    }

    complete_apps = ['precon']