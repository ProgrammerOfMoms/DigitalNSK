# Generated by Django 2.1.7 on 2019-04-15 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0020_auto_20190414_1916'),
        ('user', '0033_auto_20190415_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='events',
            field=models.ManyToManyField(blank=True, related_name='participant', to='event.Event', verbose_name='Мероприятия'),
        ),
    ]
