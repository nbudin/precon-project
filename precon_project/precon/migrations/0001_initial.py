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
            ('nonce', self.gf('django.db.models.fields.CharField')(default='87r5kb', unique=True, max_length=6)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'precon', ['Participant'])

        # Adding M2M table for field panels on 'Participant'
        m2m_table_name = db.shorten_name(u'precon_participant_panels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participant', models.ForeignKey(orm[u'precon.participant'], null=False)),
            ('panel', models.ForeignKey(orm[u'precon.panel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['participant_id', 'panel_id'])

        # Adding model 'PanelProposal'
        db.create_table(u'precon_panelproposal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('blurb', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal(u'precon', ['PanelProposal'])

        # Adding model 'PanelProposalResponse'
        db.create_table(u'precon_panelproposalresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modification_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['precon.Participant'])),
            ('panel_proposal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['precon.PanelProposal'])),
            ('attending_interest', self.gf('django.db.models.fields.CharField')(default='not interested', max_length=50)),
            ('presenting_interest', self.gf('django.db.models.fields.CharField')(default='not interested', max_length=50)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal(u'precon', ['PanelProposalResponse'])

        # Adding model 'Panel'
        db.create_table(u'precon_panel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('blurb', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal(u'precon', ['Panel'])


    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table(u'precon_participant')

        # Removing M2M table for field panels on 'Participant'
        db.delete_table(db.shorten_name(u'precon_participant_panels'))

        # Deleting model 'PanelProposal'
        db.delete_table(u'precon_panelproposal')

        # Deleting model 'PanelProposalResponse'
        db.delete_table(u'precon_panelproposalresponse')

        # Deleting model 'Panel'
        db.delete_table(u'precon_panel')


    models = {
        u'precon.panel': {
            'Meta': {'object_name': 'Panel'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'precon.panelproposal': {
            'Meta': {'object_name': 'PanelProposal'},
            'blurb': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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
            'nonce': ('django.db.models.fields.CharField', [], {'default': "'dy2ihq'", 'unique': 'True', 'max_length': '6'}),
            'panel_proposals_responded': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'participants_responded'", 'blank': 'True', 'through': u"orm['precon.PanelProposalResponse']", 'to': u"orm['precon.PanelProposal']"}),
            'panels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'panelists'", 'blank': 'True', 'to': u"orm['precon.Panel']"})
        }
    }

    complete_apps = ['precon']