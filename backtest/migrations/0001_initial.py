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
                ('json_string', models.TextField(default='')),
                ('up_votes', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Backtests',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('uuid', models.CharField(max_length=32, db_index=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('initial_balance', models.FloatField()),
                ('frequency', models.IntegerField()),
                ('num_holdings', models.IntegerField()),
                ('algorithm', models.ForeignKey(to='backtest.Algorithms')),
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
                ('backtest', models.ForeignKey(to='backtest.Backtests')),
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
        migrations.CreateModel(
            name='Ratios',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('cash_revenue', models.FloatField(null=True)),
                ('ev_ebitda', models.FloatField(null=True)),
                ('market_cap', models.FloatField(null=True)),
                ('pe_current', models.FloatField(null=True)),
                ('return_equity', models.FloatField(null=True)),
                ('stock', models.ForeignKey(to='backtest.Stocks')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreasuryBill',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('three_month', models.FloatField(null=True)),
                ('six_month', models.FloatField(null=True)),
                ('one_year', models.FloatField(null=True)),
                ('five_year', models.FloatField(null=True)),
                ('ten_year', models.FloatField(null=True)),
                ('thirty_year', models.FloatField(null=True)),
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
