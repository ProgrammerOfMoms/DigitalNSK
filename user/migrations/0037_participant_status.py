# Generated by Django 2.1.7 on 2019-04-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_auto_20190423_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='status',
            field=models.CharField(blank=True, choices=[('Ученик', 'Ученик'), ('Студент', 'Студент'), ('Бакалавр', 'Бакалавр'), ('Магистрант', 'Магистрант'), ('Аспирант', 'Аспирант'), ('Доцент', 'Доцент'), ('Профессор', 'Профессор'), ('Кандидат цифровых наук', 'Кандидат цифровых наук'), ('Доктор цифровых наук', 'Доктор цифровых наук')], default='Ученик', max_length=30, verbose_name='Статус'),
        ),
    ]