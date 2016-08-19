# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-26 20:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotes', '0003_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='likers',
            field=models.ManyToManyField(blank=True, editable=False, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
