# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('firstname', models.CharField(max_length=45)),
                ('lastname', models.CharField(max_length=45)),
                ('designation', models.CharField(max_length=5, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(max_length=10, db_index=True, unique=True)),
                ('name', models.CharField(max_length=100, db_index=True, unique=True)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MaterialProperty',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('value', models.CharField(max_length=200)),
                ('material', models.ForeignKey(to='materials.Material')),
            ],
            options={
                'verbose_name_plural': 'MaterialProperties',
            },
        ),
        migrations.CreateModel(
            name='MaterialPropertyType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('term', models.CharField(max_length=20, db_index=True, unique=True)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MaterialType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=15, db_index=True, unique=True)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Organism',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(max_length=10, db_index=True)),
                ('genus', models.CharField(max_length=45, db_index=True)),
                ('species', models.CharField(max_length=45, db_index=True)),
                ('strain', models.CharField(max_length=45, db_index=True)),
            ],
            options={
                'ordering': ['code', 'strain'],
            },
        ),
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('file', models.FileField(blank=True, upload_to='protocols')),
                ('link', models.URLField(max_length=1000, blank=True)),
                ('notes', models.CharField(max_length=400, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, db_index=True, unique=True)),
                ('building', models.CharField(max_length=100)),
                ('floor', models.CharField(max_length=25)),
                ('location', models.CharField(max_length=250, db_index=True, help_text='Room/asile etc')),
                ('temperature', models.CharField(max_length=25, db_index=True)),
                ('unit_owner', models.CharField(max_length=100, help_text='Full name of the PI owning unit. CIDResearch for centers shared properties')),
                ('unit_contact', models.EmailField(max_length=254, null=True)),
            ],
            options={
                'ordering': ['temperature', 'name'],
            },
        ),
        migrations.CreateModel(
            name='StorageInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('rack', models.CharField(max_length=5, help_text='Avoid extra text like 6th rack', verbose_name='Rack/Tower/Shelf Name:')),
                ('box', models.CharField(max_length=5, verbose_name='Box/outer container Name:')),
                ('label', models.CharField(max_length=50, verbose_name='Label of top/side of container')),
                ('quantity', models.CharField(max_length=25, default='NA', verbose_name='Quantity in ug etc')),
                ('volume', models.CharField(max_length=25, default='NA', verbose_name='Quantity in ul etc')),
                ('concentration', models.CharField(max_length=25, default='NA', verbose_name='ng/ul or 1000cells/ul etc')),
                ('date_stored', models.DateField(verbose_name='Date sample stored/frozen/received')),
                ('notebook_ref', models.CharField(max_length=100, help_text='Note Book Name:Number:Page', verbose_name='Note book Reference', null=True)),
                ('notes', models.TextField()),
                ('material', models.ForeignKey(to='materials.Material')),
                ('storage', models.ForeignKey(help_text='Stored at', verbose_name='Stored at :', to='materials.Storage')),
                ('stored_by', models.ForeignKey(to='materials.Author')),
            ],
        ),
        migrations.AddField(
            model_name='materialpropertytype',
            name='materialtype',
            field=models.ForeignKey(to='materials.MaterialType'),
        ),
        migrations.AddField(
            model_name='materialproperty',
            name='material_property_type',
            field=models.ForeignKey(to='materials.MaterialPropertyType'),
        ),
        migrations.AddField(
            model_name='material',
            name='organism',
            field=models.ForeignKey(to='materials.Organism'),
        ),
        migrations.AddField(
            model_name='material',
            name='protocol',
            field=models.ForeignKey(to='materials.Protocol'),
        ),
        migrations.AddField(
            model_name='material',
            name='type',
            field=models.ForeignKey(to='materials.MaterialType', help_text='Material Type'),
        ),
    ]
