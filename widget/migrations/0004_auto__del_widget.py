# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Widget'
        db.delete_table('widget_widget')


    def backwards(self, orm):
        
        # Adding model 'Widget'
        db.create_table('widget_widget', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('acts_on', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('widgetslot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widget.WidgetSlot'], null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('display_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'])),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('widget_module', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('widget_file_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('widget', ['Widget'])


    models = {
        'widget.widgetslot': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'WidgetSlot'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['widget']
