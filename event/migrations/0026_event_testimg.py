# Generated by Django 2.1.7 on 2019-04-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0025_auto_20190418_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='testIMG',
            field=models.ImageField(blank=True, upload_to='Events', verbose_name='Изображение1'),
        ),
    ]
