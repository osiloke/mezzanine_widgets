# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WidgetSlot'
        db.create_table('widget_widgetslot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('widget', ['WidgetSlot'])

        # Adding model 'Widget'
        db.create_table('widget_widget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('widget_module', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('acts_on', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('widgetslot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widget.WidgetSlot'], null=True)),
        ))
        db.send_create_signal('widget', ['Widget'])


    def backwards(self, orm):
        
        # Deleting model 'WidgetSlot'
        db.delete_table('widget_widgetslot')

        # Deleting model 'Widget'
        db.delete_table('widget_widget')


    models = {
        'widget.widget': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Widget'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'acts_on': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
