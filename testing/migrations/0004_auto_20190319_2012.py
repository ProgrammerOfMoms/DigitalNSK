# Generated by Django 2.1.7 on 2019-03-19 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_auto_20190311_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultOfTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competence', models.TextField(blank=True, null=True, verbose_name='Компетенция')),
            ],
            options={
                'verbose_name': 'Результат теста',
                'verbose_name_plural': 'Результаты теста',
            },
        ),
        migrations.RemoveField(
            model_name='test',
            name='question',
        ),
        migrations.AddField(
            model_name='test',
            name='mode',
            field=models.CharField(choices=[('Тест №1', 'Тест №1'), ('Тест №2', 'Тест №2'), ('Тест №3', 'Тест №3')], default='Тест №1', max_length=50, verbose_name='Тип теста'),
        ),
        migrations.AddField(
            model_name='test',
            name='questions',
            field=models.ManyToManyField(null=True, related_name='test', to='testing.Answer', verbose_name='Вопросы'),
        ),
        migrations.RemoveField(
            model_name='question',
            name='answers',
        ),
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(null=True, related_name='question', to='testing.Answer', verbose_name='Ответы'),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='resultoftest',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='testing.Test', verbose_name='Тест'),
        ),
    ]
