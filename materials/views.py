from django.shortcuts import render_to_response
from django.template import RequestContext
from materials.models import *
from materials.forms import MaterialForm, ChooseMaterialTypeForm, StorageInstanceForm, MaterialFilterForm
from materials.viewtools import *
from datetime import datetime
from collections import defaultdict

# Create your views here.


def list_organisms(request):
    """
    List all loaded Organisms. Allow exploration.
    :param request:
    :return: all Organisms objects;
    """

    kwargs = {'title': "Organisms List", 'organisms': Organism.objects.all()}
    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    return render_to_response('materials/list_organisms.html', kwargs, context_instance=RequestContext(request))


def list_storages(request):
    """
    List all freezer/storage units available. Allow exploration.
    :param request:
    :return: all Storage objects;
    """

    kwargs = {'title': "Storage/Freezer List", 'storages': Storage.objects.all()}
    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    return render_to_response('materials/list_storages.html', kwargs, context_instance=RequestContext(request))


def list_racks(request, storage_unit_id):
    """
    List all racks (or other storage units) under a freezer/sotrage unit. Allow exploration.
    :param request:
    :return: all racks from StorageInstance that belong to a particular storage unit;
    """

    kwargs = {'title': "Racks List"}
    storage = Storage.objects.get(id=storage_unit_id)
    storage_instances = StorageInstance.objects.filter(storage=storage_unit_id)
    racks = {}
    for storage_instance in storage_instances:
        racks[storage_instance.rack] = 1
    kwargs['storage'] = storage
    kwargs['racks'] = racks

    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    return render_to_response('materials/list_racks.html', kwargs, context_instance=RequestContext(request))


def list_boxes(request, storage_unit_id, rack_name):
    """
    List all racks (or other storage units) under a freezer/sotrage unit. Allow exploration.
    :param request:
    :return: all racks from StorageInstance that belong to a particular storage unit;
    """

    kwargs = {'title': "Box List"}
    storage = Storage.objects.get(id=storage_unit_id)
    storage_instances = StorageInstance.objects.filter(storage=storage_unit_id).filter(rack=rack_name)
    racks = {}
    boxes = {}
    box_info = {}
    for storage_instance in storage_instances:
        racks[storage_instance.rack] = 1
        box_info['name']=storage_instance.box
        box_info['rack']=storage_instance.rack
        boxes[storage_instance.box] = box_info

    kwargs['storage'] = storage
    kwargs['racks'] = racks
    kwargs['boxes'] = boxes

    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    return render_to_response('materials/list_boxes.html', kwargs, context_instance=RequestContext(request))


def viewbox_listview(request, storage_unit_id, rack_name, box_name):
    """
    List all materials in a box (in a rack in a storage unit)
    :param request:
    :return: all materials from box (in a rack, in a Storage unit;
    """

    kwargs = {'title': "Box view: List Layout"}
    storage_instances = StorageInstance.objects.filter(storage=storage_unit_id).filter(rack=rack_name).filter(box=box_name)

    items = {}
    for storage_instance in storage_instances:
        items[storage_instance] = storage_instance.material.materialproperty_set.all()

    kwargs['storage'] = Storage.objects.get(id=storage_unit_id)
    kwargs['rack'] = rack_name
    kwargs['box'] = box_name
    kwargs['items'] = items

    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    return render_to_response('materials/box_listview.html', kwargs, context_instance=RequestContext(request))


def viewbox_boxview(request, storage_unit_id, rack_name, box_name):
    """
    List all materials in a box (in a rack in a storage unit)
    :param request:
    :return: all materials from box (in a rack, in a Storage unit) in box layout
    """

    kwargs = {'title': "Box view: Box layout"}

    storage_instances = StorageInstance.objects.filter(storage=storage_unit_id).filter(rack=rack_name).filter(box=box_name)

    items = {}
    itemsByPosition = {}
    for storage_instance in storage_instances:
        items[storage_instance] = storage_instance.material.materialproperty_set.all()
        itemsByPosition[storage_instance.cell] = storage_instance

    kwargs['storage'] = Storage.objects.get(id=storage_unit_id)
    kwargs['rack'] = rack_name
    kwargs['box'] = box_name
    kwargs['items'] = items
    kwargs['itemsByPosition'] = itemsByPosition
    kwargs['letters'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    kwargs['numbers'] = range(1, 10)
    kwargs['material_fields'] = ['type', 'code', 'name', 'organism']
    kwargs['storageinstance_fields'] = ['label', 'volume', 'concentration', 'quantity', 'date_stored', 'storedby', 'notebook_ref']
    kwargs['timenow'] = datetime.now()

    # kwargs['user']=user
    # kwargs['listoflinks']=listoflinks

    if request.method == 'POST':
        # add only user selected fields for display
        material_fields_to_display = {'code': "YES"}
        if 'material_fields_selected' in request.POST:
            material_fields_selected = request.POST.getlist('material_fields_selected')
            for field in material_fields_selected:
                material_fields_to_display[field] = 'YES'
        kwargs['material_fields_to_display'] = material_fields_to_display

        storageinstance_fields_to_display = {}
        if 'storageinstance_fields_selected' in request.POST:
            storageinstance_fields_selected = request.POST.getlist('storageinstance_fields_selected')
            for field in storageinstance_fields_selected:
                storageinstance_fields_to_display[field] = 'YES'
        kwargs['storageinstance_fields_to_display'] = storageinstance_fields_to_display

    else:
        # minimal/base set of fields to be displayed for first time in box view
        kwargs['material_fields_to_display'] = {'type': "YES", 'code': "YES"}
        kwargs['storageinstance_fields_to_display'] = {'label': "YES"}

    return render_to_response('materials/box_boxview.html', kwargs, context_instance=RequestContext(request))


def list_materials(request):
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

    return render_to_response('materials/list_materials.html', kwargs, context_instance=RequestContext(request))


def add_material(request):
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

    return render_to_response('materials/add_material.html', kwargs, context_instance=RequestContext(request))