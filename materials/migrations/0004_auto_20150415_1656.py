# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_auto_20150415_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storageinstance',
            name='rack',
            field=models.CharField(help_text='Avoid extra text like 6th rack', verbose_name='Rack/Tower/Shelf Name:', max_length=25),
        ),
    ]
