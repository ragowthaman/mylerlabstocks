# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_auto_20150415_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storageinstance',
            name='box',
            field=models.CharField(blank=True, verbose_name='Box/outer container Name:', max_length=50),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='cell',
            field=models.CharField(blank=True, verbose_name='Row and Column number within box:', max_length=5),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='concentration',
            field=models.CharField(blank=True, default='NA', verbose_name='ng/ul or 1000cells/ul etc', max_length=25),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='date_stored',
            field=models.DateField(blank=True, verbose_name='Date sample stored/frozen/received'),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='label',
            field=models.CharField(blank=True, verbose_name='Label of top/side of container', max_length=50),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='notebook_ref',
            field=models.CharField(blank=True, default=1, verbose_name='Note book Reference', help_text='Note Book Name:Number:Page', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='quantity',
            field=models.CharField(blank=True, default='NA', verbose_name='Quantity in ug etc', max_length=25),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='volume',
            field=models.CharField(blank=True, default='NA', verbose_name='Quantity in ul etc', max_length=25),
        ),
    ]
