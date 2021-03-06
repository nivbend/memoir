# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 19:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('quotes', '0007_field_translation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('groups', models.ManyToManyField(related_name='boards', to='auth.Group')),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='board',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='quotes.Board'),
            preserve_default=False,
        ),
    ]
