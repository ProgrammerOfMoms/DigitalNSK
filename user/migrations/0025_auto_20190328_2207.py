# Generated by Django 2.1.7 on 2019-03-28 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_auto_20190325_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='competence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='testing.Group', verbose_name='Компетенция'),
        ),
    ]