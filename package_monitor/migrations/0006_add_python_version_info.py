# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package_monitor', '0005_packageversion_is_parseable'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageversion',
            name='python_support',
            field=models.CharField(default='', help_text=b'Python version support as specified in the PyPI classifiers.', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packageversion',
            name='supports_py3',
            field=models.NullBooleanField(default=None, help_text=b'Does this package support Python3?'),
        ),
    ]
