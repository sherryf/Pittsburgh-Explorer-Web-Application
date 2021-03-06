# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 19:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attractions',
            fields=[
                ('id', models.IntegerField(db_column=b'ID', primary_key=True, serialize=False)),
                ('category', models.TextField(blank=True, db_column=b'Category', null=True)),
                ('name', models.TextField(blank=True, db_column=b'Name', null=True)),
                ('imageurl', models.TextField(blank=True, db_column=b'ImageURL', null=True)),
                ('shortdesc', models.TextField(blank=True, db_column=b'ShortDesc', null=True)),
                ('recommended_length_of_visit', models.TextField(blank=True, db_column=b'Recommended_length_of_visit', null=True)),
                ('rate', models.FloatField(blank=True, db_column=b'Rate', null=True)),
                ('geocode', models.TextField(blank=True, db_column=b'Geocode', null=True)),
                ('address', models.TextField(blank=True, db_column=b'Address', null=True)),
                ('lat', models.TextField(blank=True, db_column=b'Lat', null=True)),
                ('lng', models.TextField(blank=True, db_column=b'Lng', null=True)),
                ('url', models.TextField(blank=True, db_column=b'URL', null=True)),
                ('longdesc', models.TextField(blank=True, db_column=b'LongDesc', null=True)),
                ('cost', models.FloatField(blank=True, db_column=b'Cost', null=True)),
            ],
            options={
                'db_table': 'Attractions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='InputTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(blank=True, max_length=20)),
                ('date', models.IntegerField(blank=True)),
                ('dow', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start', models.CharField(max_length=50)),
                ('starttime', models.TimeField()),
                ('interest', models.CharField(blank=True, max_length=25)),
                ('budget', models.CharField(blank=True, max_length=25)),
                ('duration1', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('duration2', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('duration3', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('duration4', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('duration5', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('event1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event1', to='planner.Attractions')),
                ('event2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event2', to='planner.Attractions')),
                ('event3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event3', to='planner.Attractions')),
                ('event4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event4', to='planner.Attractions')),
                ('event5', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event5', to='planner.Attractions')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=32)),
                ('plans', models.ManyToManyField(to='planner.Plan')),
            ],
        ),
    ]
