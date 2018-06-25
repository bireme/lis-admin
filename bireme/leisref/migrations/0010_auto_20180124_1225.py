# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leisref', '0009_auto_20180123_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actorganissuer',
            name='scope_region',
        ),
        migrations.AddField(
            model_name='actorganissuer',
            name='scope_region',
            field=models.ManyToManyField(to='leisref.ActCountryRegion', verbose_name='Country/Region', blank=True),
        ),
    ]
