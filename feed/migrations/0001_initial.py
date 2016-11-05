# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summary', models.TextField(null=True, db_index=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('location', models.TextField(null=True)),
                ('external_id', models.CharField(max_length=100, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='IcalEventSource',
            fields=[
                ('eventsource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.EventSource')),
                ('url', models.CharField(max_length=255)),
            ],
            bases=('feed.eventsource',),
        ),
        migrations.AddField(
            model_name='event',
            name='source',
            field=models.ForeignKey(to='feed.EventSource'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('source', 'external_id')]),
        ),
    ]
