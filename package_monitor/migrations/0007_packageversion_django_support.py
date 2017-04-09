# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package_monitor', '0006_add_python_version_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageversion',
            name='django_support',
            field=models.CharField(default='', help_text=b'Django version support as specified in the PyPI classifiers.', max_length=100),
            preserve_default=False,
        ),
    ]
