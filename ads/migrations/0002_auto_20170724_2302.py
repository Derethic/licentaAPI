# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_created_at',
            new_name='date_joined',
        ),
    ]