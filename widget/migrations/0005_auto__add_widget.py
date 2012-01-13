# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Widget'
        db.create_table('widget_widget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('display_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('widget_module', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('widget_file_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('acts_on', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('widgetslot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widget.WidgetSlot'], null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('widget', ['Widget'])


    def backwards(self, orm):
        
        # Deleting model 'Widget'
        db.delete_table('widget_widget')


    models = {
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
            'display_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
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
