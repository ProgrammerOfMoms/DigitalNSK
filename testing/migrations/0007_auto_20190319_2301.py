# Generated by Django 2.1.7 on 2019-03-19 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0006_auto_20190319_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField(verbose_name='Номер группы')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='additionalQuestion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_add', to='testing.Question', verbose_name='Дополнительный вопрос'),
        ),
        migrations.AddField(
            model_name='test',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='test', to='testing.Group', verbose_name='Группы'),
        ),
    ]