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
            field=models.CharField(help_text=b'Django version support as specified in the PyPI classifiers.', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='packageversion',
            name='python_support',
            field=models.CharField(help_text=b'Python version support as specified in the PyPI classifiers.', max_length=100, null=True, blank=True),
        ),
    ]
