# Generated by Django 2.1.7 on 2019-03-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20190228_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='passedTests',
            field=models.ManyToManyField(blank=True, null=True, related_name='participant', to='testing.Test', verbose_name='Завершенные тесты'),
        ),
    ]