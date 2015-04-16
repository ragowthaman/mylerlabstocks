# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genotype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('genotype', models.CharField(max_length=25, db_index=True, unique=True)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='storageinstance',
            name='cell',
            field=models.CharField(verbose_name='Row and Column number within box:', default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='material',
            name='code',
            field=models.CharField(max_length=10, help_text='Code for the new material. Must be unique. May not contain spaces', db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=100, help_text='Name for the new material. May contain spaces', db_index=True, unique=True),
        ),
        migrations.AlterField(
            model_name='materialpropertytype',
            name='term',
            field=models.CharField(max_length=20, db_index=True),
        ),
        migrations.AlterField(
            model_name='storageinstance',
            name='box',
            field=models.CharField(verbose_name='Box/outer container Name:', max_length=50),
        ),
        migrations.AddField(
            model_name='material',
            name='genotype',
            field=models.ForeignKey(to='materials.Genotype', default=1),
            preserve_default=False,
        ),
    ]
