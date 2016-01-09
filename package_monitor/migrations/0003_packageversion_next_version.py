# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import semantic_version.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('package_monitor', '0002_auto_20151126_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageversion',
            name='next_version',
            field=semantic_version.django_fields.VersionField(help_text=b'Next available version available from PyPI.', max_length=200, null=True, blank=True),
        ),
    ]
