# Generated by Django 2.1.7 on 2019-04-19 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0027_remove_event_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='testIMG',
        ),
        migrations.AddField(
            model_name='event',
            name='img',
            field=models.ImageField(blank=True, upload_to='Events', verbose_name='Изображение'),
        ),
    ]
