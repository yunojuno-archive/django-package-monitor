# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package_monitor', '0004_auto_20160109_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageversion',
            name='is_parseable',
            field=models.BooleanField(default=False, help_text=b'True if the version can be parsed as a valid semver version.', verbose_name=b'Parseable'),
        ),
    ]
