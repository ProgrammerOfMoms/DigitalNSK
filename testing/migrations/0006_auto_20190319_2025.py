# Generated by Django 2.1.7 on 2019-03-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0005_auto_20190319_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='questions',
            field=models.ManyToManyField(related_name='test', to='testing.Question', verbose_name='Вопросы'),
        ),
    ]
