# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('doc_engine_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
        ))
        db.send_create_signal('doc_engine', ['Tag'])

        # Adding model 'AccessRecord'
        db.create_table('doc_engine_accessrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('access_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('doc_engine', ['AccessRecord'])

        # Adding model 'StoredDocument'
        db.create_table('doc_engine_storeddocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=10)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(unique='True', max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('document_level', self.gf('django.db.models.fields.CharField')(default='4', max_length=1)),
        ))
        db.send_create_signal('doc_engine', ['StoredDocument'])

        # Adding unique constraint on 'StoredDocument', fields ['name', 'serial_number']
        db.create_unique('doc_engine_storeddocument', ['name', 'serial_number'])

        # Adding M2M table for field tags on 'StoredDocument'
        db.create_table('doc_engine_storeddocument_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('storeddocument', models.ForeignKey(orm['doc_engine.storeddocument'], null=False)),
            ('tag', models.ForeignKey(orm['doc_engine.tag'], null=False))
        ))
        db.create_unique('doc_engine_storeddocument_tags', ['storeddocument_id', 'tag_id'])

        # Adding M2M table for field permitted_groups on 'StoredDocument'
        db.create_table('doc_engine_storeddocument_permitted_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('storeddocument', models.ForeignKey(orm['doc_engine.storeddocument'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('doc_engine_storeddocument_permitted_groups', ['storeddocument_id', 'group_id'])

        # Adding model 'BatchRecord'
        db.create_table('doc_engine_batchrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_manufacture', self.gf('django.db.models.fields.DateField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=10)),
            ('batch_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('serial_number', self.gf('django.db.models.fields.IntegerField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('doc_engine', ['BatchRecord'])

        # Adding M2M table for field tags on 'BatchRecord'
        db.create_table('doc_engine_batchrecord_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('batchrecord', models.ForeignKey(orm['doc_engine.batchrecord'], null=False)),
            ('tag', models.ForeignKey(orm['doc_engine.tag'], null=False))
        ))
        db.create_unique('doc_engine_batchrecord_tags', ['batchrecord_id', 'tag_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'StoredDocument', fields ['name', 'serial_number']
        db.delete_unique('doc_engine_storeddocument', ['name', 'serial_number'])

        # Deleting model 'Tag'
        db.delete_table('doc_engine_tag')

        # Deleting model 'AccessRecord'
        db.delete_table('doc_engine_accessrecord')

        # Deleting model 'StoredDocument'
        db.delete_table('doc_engine_storeddocument')

        # Removing M2M table for field tags on 'StoredDocument'
        db.delete_table('doc_engine_storeddocument_tags')

        # Removing M2M table for field permitted_groups on 'StoredDocument'
        db.delete_table('doc_engine_storeddocument_permitted_groups')

        # Deleting model 'BatchRecord'
        db.delete_table('doc_engine_batchrecord')

        # Removing M2M table for field tags on 'BatchRecord'
        db.delete_table('doc_engine_batchrecord_tags')


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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'doc_engine.batchrecord': {
            'Meta': {'object_name': 'BatchRecord'},
            'batch_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_of_manufacture': ('django.db.models.fields.DateField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_doc_engine_batchrecord'", 'symmetrical': 'False', 'to': "orm['doc_engine.Tag']"}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '10'})
        },
        'doc_engine.storeddocument': {
            'Meta': {'ordering': "['name', '-date_modified']", 'unique_together': "(('name', 'serial_number'),)", 'object_name': 'StoredDocument'},
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'document_level': ('django.db.models.fields.CharField', [], {'default': "'4'", 'max_length': '1'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'permitted_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_doc_engine_storeddocument'", 'symmetrical': 'False', 'to': "orm['doc_engine.Tag']"}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '10'})
        },
        'doc_engine.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'})
        }
    }

    complete_apps = ['doc_engine']
