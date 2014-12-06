# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={},
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 6, 14, 24, 39, 366835)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.EmailField(default='none', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='id',
            field=models.AutoField(verbose_name='ID', default=0, primary_key=True, auto_created=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prices',
            name='date',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='industry',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='sector',
            field=models.CharField(max_length=100),
        ),
    ]
