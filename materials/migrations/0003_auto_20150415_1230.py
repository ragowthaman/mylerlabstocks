# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20150415_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialpropertytype',
            name='term',
            field=models.CharField(max_length=200, db_index=True),
        ),
    ]
