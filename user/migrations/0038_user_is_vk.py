# Generated by Django 2.1.7 on 2019-05-13 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0037_participant_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_vk',
            field=models.BooleanField(default=True, verbose_name='Зарегистрирован через вк'),
        ),
    ]