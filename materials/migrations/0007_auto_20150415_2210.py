# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_auto_20150415_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storageinstance',
            name='box',
            field=models.CharField(blank=True, verbose_name='Box/outer container Name:', max_length=100),
        ),
    ]
