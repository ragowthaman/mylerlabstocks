from django.db import models


# Create your models here.
class Author(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    designation = models.CharField(unique=True, max_length=5)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Organism(models.Model):
    code = models.CharField(max_length=10, db_index=True)
    genus = models.CharField(max_length=45, db_index=True)
    species = models.CharField(max_length=45, db_index=True)
    strain = models.CharField(max_length=45, db_index=True)

    class Meta:
        ordering = ['code', 'strain']

    def __str__(self):
        return self.code + '-' + self.strain


class Genotype(models.Model):
    genotype = models.CharField(max_length=25, unique=True, db_index=True)
    notes = models.TextField()

    def __str__(self):
        return self.genotype


class Protocol(models.Model):
    name = models.CharField(unique=True, max_length=50)
    file = models.FileField(upload_to="protocols", blank=True)
    link = models.URLField(max_length=1000, blank=True)
    notes = models.CharField(max_length=400, default=None)

    def __str__(self):
        return self.name


class MaterialType(models.Model):
    type = models.CharField(max_length=15, unique=True, db_index=True)
    notes = models.TextField()

    def __str__(self):
        return self.type


class Material(models.Model):
    code = models.CharField(max_length=10,  unique=True, db_index=True, help_text="Code for the new material. Must be unique. May not contain spaces")
    name = models.CharField(max_length=100, db_index=True, help_text="Name for the new material. May contain spaces")
    type = models.ForeignKey(MaterialType,  help_text="Material Type")
    organism = models.ForeignKey(Organism)
    genotype = models.ForeignKey(Genotype)
    protocol = models.ForeignKey(Protocol)
    notes = models.TextField()

    def __str__(self):
        return self.name


class MaterialPropertyType(models.Model):
    term = models.CharField(max_length=200, db_index=True)
    notes = models.TextField()
    materialtype = models.ForeignKey(MaterialType)

    def __str__(self):
        return self.term


class MaterialProperty(models.Model):
    material = models.ForeignKey(Material)
    material_property_type = models.ForeignKey(MaterialPropertyType)
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "MaterialProperties"

    def __str__(self):
        return self.material_property_type.term


class Storage(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    building = models.CharField(max_length=100)
    floor = models.CharField(max_length=25)
    location = models.CharField(max_length=250, db_index=True, help_text="Room/asile etc")
    temperature = models.CharField(max_length=25, db_index=True)
    unit_owner = models.CharField(max_length=100, help_text="Full name of the PI owning unit. CIDResearch for centers shared properties")
    unit_contact = models.EmailField(null=True)

    class Meta:
        ordering = ['temperature', 'name']

    def __str__(self):
        return self.name + ' ' + self.temperature


class StorageInstance(models.Model):
    material = models.ForeignKey(Material)
    storage = models.ForeignKey(Storage, help_text="Stored at", verbose_name="Stored at :")
    rack = models.CharField(max_length=25, verbose_name="Rack/Tower/Shelf Name:", help_text="Avoid extra text like 6th rack")
    box = models.CharField(max_length=100,  blank=True, verbose_name="Box/outer container Name:")
    cell = models.CharField(max_length=5, blank=True, verbose_name="Row and Column number within box:")
    label = models.CharField(max_length=50, blank=True, verbose_name="Label of top/side of container")
    quantity = models.CharField(max_length=25, blank=True, default='NA', verbose_name="Quantity in ug etc")
    volume = models.CharField(max_length=25, blank=True, default='NA', verbose_name="Quantity in ul etc")
    concentration = models.CharField(max_length=25, blank=True, default='NA', verbose_name="ng/ul or 1000cells/ul etc")
    date_stored = models.DateField(blank=True, verbose_name="Date sample stored/frozen/received")
    stored_by = models.ForeignKey(Author)
    notebook_ref = models.CharField(max_length=100, blank=True, verbose_name="Note book Reference", help_text="Note Book Name:Number:Page")
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.rack

