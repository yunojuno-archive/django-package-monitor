# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import semantic_version.django_fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PackageVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('raw', models.CharField(help_text=b'The line specified in the requirements file.', max_length=200)),
                ('package_name', models.CharField(help_text=b'The name of the package on PyPI.', unique=True, max_length=100)),
                ('current_version', semantic_version.django_fields.VersionField(help_text=b'The current version as specified in the requirements file. ', max_length=200, null=True, blank=True)),
                ('latest_version', semantic_version.django_fields.VersionField(help_text=b'Latest version available from PyPI.', max_length=200, null=True, blank=True)),
                ('licence', models.CharField(help_text=b'The licence used (extracted from PyPI info).', max_length=100, blank=True)),
                ('diff_status', models.CharField(default=b'unknown', help_text=b'The diff between current and latest versions. Updated via update_latest_version.', max_length=10, choices=[(b'unknown', b'Unknown'), (b'none', b'Up-to-date'), (b'major', b'Major'), (b'minor', b'Minor'), (b'patch', b'Patch'), (b'other', b'Other')])),
                ('checked_pypi_at', models.DateTimeField(help_text=b'When PyPI was last checked for this package.', null=True, blank=True)),
                ('is_editable', models.BooleanField(default=False, help_text=b"True if this requirement is specified with '-e' flag.")),
                ('url', models.URLField(help_text=b'The URL to check - PyPI or repo (if editable).', null=True, blank=True)),
            ],
        ),
    ]
