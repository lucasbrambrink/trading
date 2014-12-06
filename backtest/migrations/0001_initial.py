# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('up_votes', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price_purchased', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Portfolios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.CharField(max_length=10)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('sector', models.CharField(max_length=30)),
                ('industry', models.CharField(max_length=30)),
                ('symbol', models.CharField(max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, to=settings.AUTH_USER_MODEL, primary_key=True, auto_created=True, serialize=False)),
                ('avatar', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
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
            field=models.ForeignKey(to='backtest.Users'),
            preserve_default=True,
        ),
    ]
