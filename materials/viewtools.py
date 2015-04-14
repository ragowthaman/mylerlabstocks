from materials.models import MaterialProperty, MaterialPropertyType
#this file is to be included in views


def GetChoiceValueTuple(queryset, fieldname):
        values = queryset.values_list(fieldname, flat=True)
        unique_values = ['ALL']
        [unique_values.append(item) for item in values if item not in unique_values]
        choice_list = []
        for item in unique_values:
            choice_list.append(tuple([item, item]))
        return tuple(choice_list)

def GetChoiceValueTupleForForeignKey(queryset, fieldname):
        values = queryset.values_list(fieldname, flat=True)
        keys = queryset.values_list('id', flat=True)
        choice_list = [('ALL', 'ALL')]
        for pair in list(zip(keys, values)):
            choice_list.append(pair)

        return tuple(choice_list)

def GetChoiceValueTupleForOrganismFK(queryset, fieldname):
        code_strain_tuple = queryset.values_list('code', 'strain')
        code_strain_list = list(('-'.join(w) for w in code_strain_tuple))
        keys = queryset.values_list('id', flat=True)
        choice_list = [('ALL', 'ALL')]
        for pair in list(zip(keys, code_strain_list)):
            choice_list.append(pair)

        return tuple(choice_list)


def save_materialproperty(material_object, property_name, property_value):
    newobject = MaterialProperty()
    newobject.material = material_object
    newobject.material_property_type = MaterialPropertyType.objects.get(term=property_name)
    newobject.value = property_value
    newobject.save()