# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_archived', models.BooleanField(default=False)),
                ('name', models.TextField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_archived', models.BooleanField(default=False)),
                ('title', models.TextField(max_length=50)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_archived', models.BooleanField(default=False)),
                ('title', models.TextField(max_length=50)),
                ('order', models.IntegerField()),
                ('board', models.ForeignKey(to='taskboard.Board', related_name='columns')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50)),
                ('board', models.ForeignKey(to='taskboard.Board', related_name='labels')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_archived', models.BooleanField(default=False)),
                ('name', models.TextField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together=set([('title', 'board')]),
        ),
        migrations.AlterUniqueTogether(
            name='column',
            unique_together=set([('title', 'board')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='column',
            order_with_respect_to='board',
        ),
        migrations.AddField(
            model_name='card',
            name='column',
            field=models.ForeignKey(to='taskboard.Column', related_name='cards'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='label',
            field=models.ForeignKey(to='taskboard.Label'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='members',
            field=models.ManyToManyField(to='taskboard.Member', related_name='cards'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='card',
            order_with_respect_to='column',
        ),
    ]
