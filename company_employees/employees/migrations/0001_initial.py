# Generated by Django 2.1.1 on 2019-04-15 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
                ('birth', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12)),
                ('start_work', models.DateField(auto_now_add=True)),
                ('finish_work', models.DateField(null=True)),
                ('position', models.CharField(max_length=32)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit')),
            ],
        ),
    ]
