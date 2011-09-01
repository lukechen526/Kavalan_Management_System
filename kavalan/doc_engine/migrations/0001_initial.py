# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DocumentLabel'
        db.create_table('doc_engine_documentlabel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('doc_engine', ['DocumentLabel'])

        # Adding model 'Document'
        db.create_table('doc_engine_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(unique='True', max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.CharField')(default='Wufulab Ltd', max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=10)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('document_level', self.gf('django.db.models.fields.CharField')(default='4', max_length=1)),
            ('searchable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('doc_engine', ['Document'])

        # Adding M2M table for field labels on 'Document'
        db.create_table('doc_engine_document_labels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm['doc_engine.document'], null=False)),
            ('documentlabel', models.ForeignKey(orm['doc_engine.documentlabel'], null=False))
        ))
        db.create_unique('doc_engine_document_labels', ['document_id', 'documentlabel_id'])

        # Adding M2M table for field permitted_groups on 'Document'
        db.create_table('doc_engine_document_permitted_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('document', models.ForeignKey(orm['doc_engine.document'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('doc_engine_document_permitted_groups', ['document_id', 'group_id'])

        # Adding model 'FileObject'
        db.create_table('doc_engine_fileobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['doc_engine.Document'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('uploaded_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('revision_comment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('doc_engine', ['FileObject'])

        # Adding model 'AccessRecord'
        db.create_table('doc_engine_accessrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('access_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('document_accessed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doc_engine.Document'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('doc_engine', ['AccessRecord'])

        # Adding model 'BatchRecord'
        db.create_table('doc_engine_batchrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('batch_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('serial_number', self.gf('django.db.models.fields.IntegerField')()),
            ('date_manufactured', self.gf('django.db.models.fields.DateField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('doc_engine', ['BatchRecord'])


    def backwards(self, orm):
        
        # Deleting model 'DocumentLabel'
        db.delete_table('doc_engine_documentlabel')

        # Deleting model 'Document'
        db.delete_table('doc_engine_document')

        # Removing M2M table for field labels on 'Document'
        db.delete_table('doc_engine_document_labels')

        # Removing M2M table for field permitted_groups on 'Document'
        db.delete_table('doc_engine_document_permitted_groups')

        # Deleting model 'FileObject'
        db.delete_table('doc_engine_fileobject')

        # Deleting model 'AccessRecord'
        db.delete_table('doc_engine_accessrecord')

        # Deleting model 'BatchRecord'
        db.delete_table('doc_engine_batchrecord')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'doc_engine.accessrecord': {
            'Meta': {'ordering': "['-access_time', 'user']", 'object_name': 'AccessRecord'},
            'access_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document_accessed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doc_engine.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'doc_engine.batchrecord': {
            'Meta': {'object_name': 'BatchRecord'},
            'batch_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date_manufactured': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {})
        },
        'doc_engine.document': {
            'Meta': {'object_name': 'Document'},
            'author': ('django.db.models.fields.CharField', [], {'default': "'Wufulab Ltd'", 'max_length': '100'}),
            'document_level': ('django.db.models.fields.CharField', [], {'default': "'4'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['doc_engine.DocumentLabel']", 'symmetrical': 'False', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'permitted_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'searchable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '10'})
        },
        'doc_engine.documentlabel': {
            'Meta': {'object_name': 'DocumentLabel'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'doc_engine.fileobject': {
            'Meta': {'object_name': 'FileObject'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['doc_engine.Document']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision_comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'uploaded_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['doc_engine']
