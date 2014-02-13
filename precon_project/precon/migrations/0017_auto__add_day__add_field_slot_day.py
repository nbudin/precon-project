# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Day'
        db.create_table(u'precon_day', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'precon', ['Day'])

        # Adding field 'Slot.day'
        db.add_column(u'precon_slot', 'day',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['precon.Day'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Day'
        db.delete_table(u'precon_day')

        # Deleting field 'Slot.day'
        db.delete_column(u'precon_slot', 'day_id')


    models = {
        u'precon.day': {
            'Meta': {'object_name': 'Day'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'precon.panel': {
            'Meta': {'ordering': "['name']", 'object_name': 'Panel'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'panel_proposal': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'panels_accepted'", 'null': 'True', 'to': u"orm['precon.PanelProposal']"}),
            'panelists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'panels'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['precon.Panelist']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'panels'", 'null': 'True', 'to': u"orm['precon.Room']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'panels'", 'null': 'True', 'to': u"orm['precon.Slot']"}),
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
            'nonce': ('django.db.models.fields.CharField', [], {'default': "'u5kdn9'", 'unique': 'True', 'max_length': '6'}),
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
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.Day']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slots'", 'to': u"orm['precon.Schedule']"})
        }
    }

    complete_apps = ['precon']