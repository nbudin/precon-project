# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Slot.datetime'
        db.delete_column(u'precon_slot', 'datetime')

        # Adding field 'Slot.name'
        db.add_column(u'precon_slot', 'name',
                      self.gf('django.db.models.fields.CharField')(default='(unnamed)', max_length=20),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Slot.datetime'
        raise RuntimeError("Cannot reverse this migration. 'Slot.datetime' and its values cannot be restored.")
        # Deleting field 'Slot.name'
        db.delete_column(u'precon_slot', 'name')


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
            'attending_comments': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'attending_interest': ('django.db.models.fields.CharField', [], {'default': "'not interested'", 'max_length': '50'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'panel_proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.PanelProposal']"}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.Participant']"}),
            'presenting_comments': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
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
            'nonce': ('django.db.models.fields.CharField', [], {'default': "'y89j0c'", 'unique': 'True', 'max_length': '6'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'slots'", 'to': u"orm['precon.Schedule']"})
        }
    }

    complete_apps = ['precon']