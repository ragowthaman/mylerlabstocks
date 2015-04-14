from django.shortcuts import render_to_response
from django.template import RequestContext
from materials.models import *
from materials.forms import MaterialForm, ChooseMaterialTypeForm, StorageInstanceForm, MaterialFilterForm
from materials.viewtools import *

# Create your views here.


def organisms_list(request):
    """
    List all loaded Organisms. Allow exploration.
    :param request:
    :return: all Organisms objects;
    """

    kwargs = {'title': "Organisms List", 'organisms': Organism.objects.all()}
    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    return render_to_response('materials/organisms_list.html', kwargs, context_instance=RequestContext(request))


def material_list(request):
    """
    List all loaded materials. Allow exploration.
    :param request:
    :return: all Organisms objects;
    """

    kwargs = {'title': "Materials List"}
    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks
    form = MaterialFilterForm(request.POST or None)
    kwargs['form'] = form
    materials = Material.objects.all()
    print(form)
    if request.method == 'POST':
        for key, value in form.cleaned_data.items():
            if (value != 'ALL') & (value != ''):
                if (key == 'code') | (key == 'name'):
                    key += '__icontains'
                materials = materials.filter(**{key: value})

    kwargs['materials'] = materials

    return render_to_response('materials/material_list.html', kwargs, context_instance=RequestContext(request))


def material_add(request):
    """
    Add a new material to the database
    :param request:
    :return: display form to select type of material
    """

    kwargs = {'title': "Add Materials: Choose Material Type"}
    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    if request.method == 'POST':
        # when user is just chose the material type (step1)
        if 'chooseMaterialType' in request.POST:
            chooseform = ChooseMaterialTypeForm(request.POST)
            if chooseform.is_valid():
                materialtype = chooseform.cleaned_data['materialtype']
                kwargs['materialtype'] = materialtype
                # Get Material form with material type specific fields custom added to it
                kwargs['materialform'] = MaterialForm(materialtype=materialtype)
                kwargs['storageinstanceform'] = StorageInstanceForm()

            else:
                kwargs['chooseform'] = chooseform

        # if user filled in details for the material already (step2)
        elif 'addMaterial' in request.POST:
            materialtype_id = request.POST['type']
            materialform = MaterialForm(request.POST, materialtype=str(MaterialType.objects.get(id=materialtype_id)))
            storageinstanceform = StorageInstanceForm(request.POST)

            if materialform.is_valid() & storageinstanceform.is_valid():
                print("both forms are valid, now adding to database")
                # save material object
                material_object = materialform.save()

                # save material properties
                for (property_name, property_value) in materialform.get_material_properties():
                    print(property_name, ':', property_value)
                    save_materialproperty(material_object, property_name, property_value)

                # saver storage instance
                sotrageinstance = storageinstanceform.save(commit=False)
                sotrageinstance.material = material_object
                sotrageinstance.save()

                # save sucesses
                kwargs['save_sucesses'] = 'save_sucesses'

            else:
                print("One or both forms are NOT valid, Can not add to database")
                # one or both forms are NOT valid
                kwargs['materialtype'] = 'materialtype'
                kwargs['materialform'] = materialform
                kwargs['storageinstanceform'] = storageinstanceform

    else:
        #form is accessed for fist time
        kwargs['chooseform'] = ChooseMaterialTypeForm()

    return render_to_response('materials/material_add.html', kwargs, context_instance=RequestContext(request))