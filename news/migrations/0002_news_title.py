# Generated by Django 2.1.7 on 2019-04-17 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.TextField(default='title', verbose_name='Заголовок'),
        ),
    ]
