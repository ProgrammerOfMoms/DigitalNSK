# Generated by Django 2.1.7 on 2019-04-10 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20190409_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='count',
        ),
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='event',
            name='format_task',
        ),
    ]