# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-18 10:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musterroll', '0002_remove_employeeseparation_final_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noduesemp',
            name='head_id',
            field=models.ForeignKey(blank=True, db_column='Head_Id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp_id_head', to='musterroll.NoDuesHead'),
        ),
    ]
