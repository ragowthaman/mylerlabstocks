from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Author)
admin.site.register(Organism)
admin.site.register(Protocol)

class MaterialTypeAdmin(admin.ModelAdmin):
    fields=['type', 'notes']
    list_display=('type', 'notes')
admin.site.register(MaterialType, MaterialTypeAdmin)

class MaterialPropertyInline(admin.TabularInline):
    model = MaterialProperty
    extra = 5

class SotrageInstanceInline(admin.TabularInline):
    model = StorageInstance
    extra = 3

class MaterialAdmin(admin.ModelAdmin):
    fields = ['code', 'name', 'type', 'organism', 'protocol', 'notes']
    list_display = ['code', 'name', 'type', 'organism', 'protocol', 'notes']
    inlines = [MaterialPropertyInline, SotrageInstanceInline]

admin.site.register(Material, MaterialAdmin)

admin.site.register(MaterialPropertyType)
admin.site.register(MaterialProperty)
admin.site.register(Storage)


admin.site.register(StorageInstance)
