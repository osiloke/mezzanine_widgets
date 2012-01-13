# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Widget.keywords_string'
        db.add_column('widget_widget', 'keywords_string', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True), keep_default=False)

        # Adding field 'Widget.slug'
        db.add_column('widget_widget', 'slug', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Widget.status'
        db.add_column('widget_widget', 'status', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Widget.publish_date'
        db.add_column('widget_widget', 'publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Widget.expiry_date'
        db.add_column('widget_widget', 'expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Widget.description'
        db.add_column('widget_widget', 'description', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Widget.short_url'
        db.add_column('widget_widget', 'short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'Widget.site'
        db.add_column('widget_widget', 'site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']), keep_default=False)

        # Adding field 'Widget.widget_file_title'
        db.add_column('widget_widget', 'widget_file_title', self.gf('django.db.models.fields.CharField')(default='Default', max_length=255), keep_default=False)

        # Changing field 'Widget.title'
        db.alter_column('widget_widget', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))


    def backwards(self, orm):
        
        # Deleting field 'Widget.keywords_string'
        db.delete_column('widget_widget', 'keywords_string')

        # Deleting field 'Widget.slug'
        db.delete_column('widget_widget', 'slug')

        # Deleting field 'Widget.status'
        db.delete_column('widget_widget', 'status')

        # Deleting field 'Widget.publish_date'
        db.delete_column('widget_widget', 'publish_date')

        # Deleting field 'Widget.expiry_date'
        db.delete_column('widget_widget', 'expiry_date')

        # Deleting field 'Widget.description'
        db.delete_column('widget_widget', 'description')

        # Deleting field 'Widget.short_url'
        db.delete_column('widget_widget', 'short_url')

        # Deleting field 'Widget.site'
        db.delete_column('widget_widget', 'site_id')

        # Deleting field 'Widget.widget_file_title'
        db.delete_column('widget_widget', 'widget_file_title')

        # Changing field 'Widget.title'
        db.alter_column('widget_widget', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic.assignedkeyword': {
            'Meta': {'object_name': 'AssignedKeyword'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'widget.widget': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Widget'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'acts_on': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.AssignedKeyword']"}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'widget_file_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widget_module': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'widgetslot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['widget.WidgetSlot']", 'null': 'True'})
        },
        'widget.widgetslot': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'WidgetSlot'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['widget']
