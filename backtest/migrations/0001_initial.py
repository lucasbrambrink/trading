# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithms',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('up_votes', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('price_purchased', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AT_Users',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Portfolios',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('blocks', models.CharField(max_length=50)),
                ('balance', models.CharField(max_length=25)),
                ('algorithm', models.ForeignKey(to='backtest.Algorithms')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.CharField(max_length=15)),
                ('open', models.CharField(max_length=20)),
                ('high', models.CharField(max_length=20)),
                ('low', models.CharField(max_length=20)),
                ('close', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('sector', models.CharField(max_length=100)),
                ('industry', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=6)),
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
        migrations.AddField(
            model_name='assets',
            name='portfolio',
            field=models.ForeignKey(to='backtest.Portfolios'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assets',
            name='stock',
            field=models.ForeignKey(to='backtest.Stocks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='algorithms',
            name='created_by',
            field=models.ForeignKey(to='backtest.AT_Users'),
            preserve_default=True,
        ),
    ]
