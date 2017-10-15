# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-22 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_auto_20161205_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='choices',
            field=models.CharField(help_text='[{"text": "Alain Juppé", "slug": "alain-juppe"}, {"text": "François Fillon", "slug": "francois-fillon"}]', max_length=1024),
        ),
    ]