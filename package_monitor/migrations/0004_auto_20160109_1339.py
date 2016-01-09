# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package_monitor', '0003_packageversion_next_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packageversion',
            name='is_editable',
            field=models.BooleanField(default=False, help_text=b"True if this requirement is specified with '-e' flag.", verbose_name=b'Editable (-e)'),
        ),
        migrations.AlterField(
            model_name='packageversion',
            name='url',
            field=models.URLField(help_text=b'The PyPI URL to check - (blank if editable).', null=True, blank=True),
        ),
    ]
