# Generated by Django 2.1.7 on 2019-04-17 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_code', models.TextField(verbose_name='html код новости')),
                ('photo', models.TextField(verbose_name='Картинка к новости')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
