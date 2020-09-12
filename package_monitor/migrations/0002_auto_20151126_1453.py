# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("package_monitor", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="packageversion",
            options={
                "ordering": ["package_name"],
                "verbose_name_plural": "Package versions",
            },
        ),
    ]
