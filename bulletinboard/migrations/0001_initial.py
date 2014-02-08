# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'bulletinboard_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('user_type', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('is_banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')()),
            ('birthdate', self.gf('django.db.models.fields.DateField')()),
            ('hometown', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('present_location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('ym', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1)),
            ('interests', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'bulletinboard', ['UserProfile'])

        # Adding model 'Topic'
        db.create_table(u'bulletinboard_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'bulletinboard', ['Topic'])

        # Adding model 'Board'
        db.create_table(u'bulletinboard_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulletinboard.Topic'])),
            ('rank', self.gf('django.db.models.fields.SmallIntegerField')(unique=True, db_index=True)),
        ))
        db.send_create_signal(u'bulletinboard', ['Board'])

        # Adding model 'Thread'
        db.create_table(u'bulletinboard_thread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulletinboard.UserProfile'])),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulletinboard.Board'])),
            ('thread_type', self.gf('django.db.models.fields.CharField')(default=2, max_length=1)),
            ('is_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bulletinboard', ['Thread'])

        # Adding model 'Post'
        db.create_table(u'bulletinboard_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulletinboard.UserProfile'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulletinboard.Thread'])),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('message_markdown', self.gf('django.db.models.fields.TextField')()),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'bulletinboard', ['Post'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'bulletinboard_userprofile')

        # Deleting model 'Topic'
        db.delete_table(u'bulletinboard_topic')

        # Deleting model 'Board'
        db.delete_table(u'bulletinboard_board')

        # Deleting model 'Thread'
        db.delete_table(u'bulletinboard_thread')

        # Deleting model 'Post'
        db.delete_table(u'bulletinboard_post')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bulletinboard.board': {
            'Meta': {'ordering': "('rank',)", 'object_name': 'Board'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulletinboard.Topic']"})
        },
        u'bulletinboard.post': {
            'Meta': {'ordering': "('date_posted',)", 'object_name': 'Post'},
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'message_markdown': ('django.db.models.fields.TextField', [], {}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulletinboard.Thread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulletinboard.UserProfile']"})
        },
        u'bulletinboard.thread': {
            'Meta': {'ordering': "('thread_type',)", 'object_name': 'Thread'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulletinboard.Board']"}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'thread_type': ('django.db.models.fields.CharField', [], {'default': '2', 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulletinboard.UserProfile']"})
        },
        u'bulletinboard.topic': {
            'Meta': {'object_name': 'Topic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bulletinboard.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.TextField', [], {}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'hometown': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'present_location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ym': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bulletinboard']