# Generated by Django 2.1.7 on 2019-04-18 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0024_remove_event_maincompetence'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='mainComp',
            new_name='mainCompetence',
        ),
    ]