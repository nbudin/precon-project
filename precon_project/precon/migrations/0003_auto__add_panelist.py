# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Panelist'
        db.create_table(u'precon_panelist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['precon.Participant'], blank=True)),
        ))
        db.send_create_signal(u'precon', ['Panelist'])

        # Adding M2M table for field panelists on 'PanelProposal'
        m2m_table_name = db.shorten_name(u'precon_panelproposal_panelists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('panelproposal', models.ForeignKey(orm[u'precon.panelproposal'], null=False)),
            ('panelist', models.ForeignKey(orm[u'precon.panelist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['panelproposal_id', 'panelist_id'])

        # Adding M2M table for field panelists on 'Panel'
        m2m_table_name = db.shorten_name(u'precon_panel_panelists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('panel', models.ForeignKey(orm[u'precon.panel'], null=False)),
            ('panelist', models.ForeignKey(orm[u'precon.panelist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['panel_id', 'panelist_id'])

        # Removing M2M table for field panels on 'Participant'
        db.delete_table(db.shorten_name(u'precon_participant_panels'))


    def backwards(self, orm):
        # Deleting model 'Panelist'
        db.delete_table(u'precon_panelist')

        # Removing M2M table for field panelists on 'PanelProposal'
        db.delete_table(db.shorten_name(u'precon_panelproposal_panelists'))

        # Removing M2M table for field panelists on 'Panel'
        db.delete_table(db.shorten_name(u'precon_panel_panelists'))

        # Adding M2M table for field panels on 'Participant'
        m2m_table_name = db.shorten_name(u'precon_participant_panels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm[u'precon.participant'], null=False)),
            ('panel', models.ForeignKey(orm[u'precon.panel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['participant_id', 'panel_id'])


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
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['precon.Participant']", 'blank': 'True'})
        },
        u'precon.panelproposal': {
            'Meta': {'object_name': 'PanelProposal'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'needs_panelists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'panelists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['precon.Panelist']", 'symmetrical': 'False', 'blank': 'True'})
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
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'nonce': ('django.db.models.fields.CharField', [], {'default': "'3407s2'", 'unique': 'True', 'max_length': '6'}),
            'panel_proposals_responded': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'participants_responded'", 'blank': 'True', 'through': u"orm['precon.PanelProposalResponse']", 'to': u"orm['precon.PanelProposal']"})
        }
    }

    complete_apps = ['precon']