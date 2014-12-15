# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('uuid', models.CharField(db_index=True, max_length=32)),
                ('name', models.CharField(max_length=30)),
                ('up_votes', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('quantity', models.IntegerField()),
                ('price_purchased', models.FloatField()),
                ('date', models.DateField()),
                ('algorithm', models.ForeignKey(to='backtest.Algorithms')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('sector', models.CharField(max_length=100)),
                ('industry', models.CharField(max_length=100)),
                ('symbol', models.CharField(db_index=True, max_length=6, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prices',
            name='stock',
            field=models.ForeignKey(to='backtest.Stocks'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='prices',
            unique_together=set([('stock', 'date')]),
        ),
        migrations.AddField(
            model_name='assets',
            name='stock',
            field=models.ForeignKey(to='backtest.Stocks'),
            preserve_default=True,
        ),
    ]
