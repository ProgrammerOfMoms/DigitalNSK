# Generated by Django 2.1.7 on 2019-04-30 16:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(default=datetime.date(2019, 4, 30), verbose_name='Дата публикации'),
        ),
    ]
