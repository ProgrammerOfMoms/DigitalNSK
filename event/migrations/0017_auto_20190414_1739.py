# Generated by Django 2.1.7 on 2019-04-14 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0016_auto_20190414_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecompetence',
            name='subCompetence',
            field=models.ManyToManyField(related_name='baseComp', to='event.SideCompetence', verbose_name='Субкомпетенции 3 уровня'),
        ),
    ]
