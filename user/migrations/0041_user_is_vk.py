# Generated by Django 2.1.7 on 2019-05-14 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0040_remove_user_is_vk'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_vk',
            field=models.BooleanField(default=False, verbose_name='Зарегистрирован через вк'),
        ),
    ]
