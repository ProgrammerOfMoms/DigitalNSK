# Generated by Django 2.1.7 on 2019-03-28 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_auto_20190328_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='competence',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Компетенция'),
        ),
    ]
