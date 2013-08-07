# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SchoolData'
        db.create_table(u'data_schooldata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('EMIS_id_school_data', self.gf('django.db.models.fields.related.ForeignKey')(related_name='EMIS_id_school_data', to=orm['hierarchy.School'])),
            ('classroom_total', self.gf('django.db.models.fields.IntegerField')()),
            ('teachers_total', self.gf('django.db.models.fields.IntegerField')()),
            ('g1_teachers', self.gf('django.db.models.fields.IntegerField')()),
            ('g2_teachers', self.gf('django.db.models.fields.IntegerField')()),
            ('boys_total', self.gf('django.db.models.fields.IntegerField')()),
            ('girls_total', self.gf('django.db.models.fields.IntegerField')()),
            ('g2_boys', self.gf('django.db.models.fields.IntegerField')()),
            ('g2_girls', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'data', ['SchoolData'])

        # Adding model 'HeadTeacher'
        db.create_table(u'data_headteacher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('is_zonal_head', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('EMIS_id_header_teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='EMIS_id_header_teacher', to=orm['hierarchy.School'])),
            ('year', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'data', ['HeadTeacher'])


    def backwards(self, orm):
        # Deleting model 'SchoolData'
        db.delete_table(u'data_schooldata')

        # Deleting model 'HeadTeacher'
        db.delete_table(u'data_headteacher')


    models = {
        u'data.headteacher': {
            'EMIS_id_header_teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'EMIS_id_header_teacher'", 'to': u"orm['hierarchy.School']"}),
            'Meta': {'object_name': 'HeadTeacher'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_zonal_head': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'year': ('django.db.models.fields.DateField', [], {})
        },
        u'data.schooldata': {
            'EMIS_id_school_data': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'EMIS_id_school_data'", 'to': u"orm['hierarchy.School']"}),
            'Meta': {'object_name': 'SchoolData'},
            'boys_total': ('django.db.models.fields.IntegerField', [], {}),
            'classroom_total': ('django.db.models.fields.IntegerField', [], {}),
            'g1_teachers': ('django.db.models.fields.IntegerField', [], {}),
            'g2_boys': ('django.db.models.fields.IntegerField', [], {}),
            'g2_girls': ('django.db.models.fields.IntegerField', [], {}),
            'g2_teachers': ('django.db.models.fields.IntegerField', [], {}),
            'girls_total': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teachers_total': ('django.db.models.fields.IntegerField', [], {})
        },
        u'hierarchy.district': {
            'Meta': {'object_name': 'District'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'province_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'province_id'", 'to': u"orm['hierarchy.Province']"})
        },
        u'hierarchy.province': {
            'Meta': {'object_name': 'Province'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hierarchy.school': {
            'EMIS': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'School'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zone_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zone_id'", 'to': u"orm['hierarchy.Zone']"})
        },
        u'hierarchy.zone': {
            'Meta': {'object_name': 'Zone'},
            'district_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_id'", 'to': u"orm['hierarchy.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['data']