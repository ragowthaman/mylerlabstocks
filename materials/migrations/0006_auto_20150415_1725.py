# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_auto_20150415_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(db_index=True, help_text='Name for the new material. May contain spaces', max_length=100),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
