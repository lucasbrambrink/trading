# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prices',
            name='volume',
            field=models.CharField(max_length=20, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prices',
            name='date',
            field=models.DateField(),
        ),
    ]
