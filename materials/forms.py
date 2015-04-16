from django import forms
from materials.models import Material, MaterialType, StorageInstance, Organism, Protocol
from materials.viewtools import *


class ChooseMaterialTypeForm(forms.Form):
    materialtype = forms.ChoiceField(choices=GetChoiceValueTuple(MaterialType.objects.all(), 'type'))


class MaterialForm(forms.ModelForm):
    code = forms.CharField(max_length=10, help_text="Enter a code for the new material")
    notes = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Material
        fields = ('code', 'name', 'type', 'organism', 'protocol', 'genotype')

    # Now add MaterialType specific MaterialProperty fields to the form
    def __init__(self, *args, **kwargs):
        # get material type
        materialtype = kwargs.pop('materialtype')

        # get propertyTerms for given material type
        material_property_terms = MaterialPropertyType.objects.filter(materialtype=MaterialType.objects.get(type=materialtype)).values_list('term', flat=True)
        super(MaterialForm, self).__init__(*args, **kwargs)

        for key in material_property_terms:
            self.fields['custom_%s' % key] = forms.CharField(label=key, help_text=key.replace('_', ' '))

    # Now a function to parse the custom data [field names starts with custom]
    def get_material_properties(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)


class StorageInstanceForm(forms.ModelForm):
    rack = forms.CharField(max_length=10, help_text="Avoid extra text like 6th rack")

    class Meta:
        model = StorageInstance
        fields = ('material', 'storage', 'rack', 'box', 'cell', 'label', 'quantity', 'volume', 'concentration', 'date_stored', 'stored_by', 'notebook_ref', 'notes')


class MaterialFilterForm(forms.Form):
    code = forms.CharField(max_length=10, help_text="Enter a code for the new material", required=False)
    name = forms.CharField(max_length=10, help_text="Enter a code for the new material", required=False)
    type = forms.ChoiceField(choices=GetChoiceValueTupleForForeignKey(MaterialType.objects.all(), 'type'), required=False)
    organism = forms.ChoiceField(choices=GetChoiceValueTupleForOrganismFK(Organism.objects.all(), 'code'), required=False)
    protocol = forms.ChoiceField(choices=GetChoiceValueTupleForForeignKey(Protocol.objects.all(), 'name'), required=False)
