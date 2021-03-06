# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 22:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_auto_20161124_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('description', models.TextField(max_length=5000)),
                ('choices', models.CharField(max_length=1024)),
            ],
            options={
                'get_latest_by': 'start',
                'verbose_name': 'élection',
            },
        ),
        migrations.AddField(
            model_name='vote',
            name='election',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vote.Election'),
            preserve_default=False,
        ),
    ]
