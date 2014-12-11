# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0002_auto_20141211_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithms',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='assets',
            name='portfolio',
        ),
        migrations.DeleteModel(
            name='Portfolios',
        ),
        migrations.AddField(
            model_name='assets',
            name='algorithm',
            field=models.ForeignKey(default=None, to='backtest.Algorithms'),
            preserve_default=False,
        ),
    ]
