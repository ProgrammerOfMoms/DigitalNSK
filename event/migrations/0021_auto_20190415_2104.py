# Generated by Django 2.1.7 on 2019-04-15 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0020_auto_20190414_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basecompetence',
            name='subCompetence',
        ),
        migrations.RemoveField(
            model_name='maincompetence',
            name='subCompetence',
        ),
        migrations.RemoveField(
            model_name='sidecompetenceadd',
            name='subCompetence',
        ),
    ]
