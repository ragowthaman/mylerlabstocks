#!/Users/gramasamy/virtualenv/mylerlabstocks/bin/python

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import os
import xlrd
import sys
import time
from datetime import datetime
sys.path.append('/Users/gramasamy/djcode/mylerlabstocks/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mylerlabstocks.settings'
from materials.models import *


################################################################################
#
#  Functions
#################################################################################

def argparse():
    '''parses the command line arguments'''
    import argparse
    parser = argparse.ArgumentParser(description='Uploads the Stabilates data into postgress database for Django application')
    parser.add_argument('--legacyDataSheet', required=True, help='the spread sheet with legacy data in one tab')
    parser.add_argument('--debug', required=False, default=False, type=bool)
    parser.add_argument('--version', '-v',  action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    return args

def excelDateValue2timeStampStr(cellValue, outFormat):
    datetimeTimeStampStr = 'No'
    if cellValue:
        cellTuple = xlrd.xldate_as_tuple(cellValue, 0) + (0, 0, 0)
        datetimeTimeStamp    = datetime.fromtimestamp(time.mktime(cellTuple))
        datetimeTimeStampStr = datetimeTimeStamp.strftime(outFormat)
    return datetimeTimeStampStr



################################################################################
#
#  Main
#################################################################################
# delete objects:
# Material.objects.all().delete()
# MaterialProperty.objects.all().delete()
# StorageInstance.objects.all().delete()

args = argparse()
legacyDataSheet = args.legacyDataSheet

workbook = xlrd.open_workbook(legacyDataSheet)
datatab = workbook.sheet_by_index(0)
#excelDateValue2timeStampStr(row_content[5].value, outFormat = '%m/%d/%y %H:%M:%S'),
for row_index in range(3, datatab.nrows):
    row_content = datatab.row(row_index)
    #print(row_content)
    #print row_content
    [ uid, organism, genotype, name, label, date_stored, stored_by, box, cell, is_transformed, episomal_or_stable, anitbiotics, clone_used_in_transformation, notebook_ref, notes, stabili_name_prior_to_transformation, clones_used_in_prior_transformation, purpose_of_transformation, WHO_designation, LRV1, LD1, Reference ] = [ int(row_content[0].value), row_content[1].value.rstrip(), row_content[2].value.rstrip(), row_content[3].value.rstrip(), row_content[4].value.rstrip(), row_content[5].value, row_content[6].value.rstrip(), row_content[7].value.rstrip(), row_content[8].value.rstrip(), row_content[9].value.rstrip(), row_content[10].value.rstrip(), row_content[11].value.rstrip(), row_content[12].value.rstrip(), row_content[13].value.rstrip(), row_content[14].value.rstrip(), row_content[15].value.rstrip(), row_content[16].value.rstrip(), row_content[17].value.rstrip(), row_content[18].value.rstrip(), row_content[19].value.rstrip(), row_content[20].value.rstrip(), row_content[21].value.rstrip()]
    print(uid)
    material_properties = list(zip(['is_transformed', 'episomal_or_stable', 'antibiotics', 'clone_code', 'stabili_name_prior_to_transformation', 'clones_used_in_prior_transformation', 'purpose_of_transformation', 'WHO_designation', 'LRV1', 'LD1', 'Reference'], [row_content[9].value.rstrip(), row_content[10].value.rstrip(), row_content[11].value.rstrip(), row_content[12].value.rstrip(), row_content[15].value.rstrip(), row_content[16].value.rstrip(), row_content[17].value.rstrip(), row_content[18].value.rstrip(), row_content[19].value.rstrip(), row_content[20].value.rstrip(), row_content[21].value.rstrip()]))

    stored_by_list = stored_by.split(" ")

    if date_stored == 'Blank':
        date_stored = '1000-01-01'
    else:
        date_stored = excelDateValue2timeStampStr(row_content[5].value, outFormat='%Y-%m-%d')
    print(date_stored)
    orgdic = {'L. donovani 1S':5, 'L. tarentolae TarII': 6, 'L. major Friedlin': 1, 'T. cruzi YC': 10, 'T. cruzi CR Brener': 11, 'L. braziliensis M2904': 8, 'T. brucei 927': 9, 'L. donovani Bob': 7}
    genotypeObj = Genotype.objects.get(genotype=genotype)
    organismObj = Organism.objects.get(id=orgdic[organism])
    typeObj = MaterialType.objects.get(type="Stabilate")
    protocolObj = Protocol.objects.get(name='test')

    material_instance = Material(genotype=genotypeObj, organism=organismObj, type=typeObj, protocol=protocolObj)
    material_instance.code = uid
    material_instance.name = name
    material_instance.notes = notes
    material_instance.save()

    # Now save material properties
    for pair in material_properties:
        print(pair)
        materialproperty_instance = MaterialProperty(material=material_instance)
        materialproperty_instance.material_property_type = MaterialPropertyType.objects.get(term=pair[0])
        materialproperty_instance.value = pair[1]
        materialproperty_instance.save()

    # Now save storage instance
    storageinstance_instance = StorageInstance(material=material_instance)
    storageinstance_instance.storage = Storage.objects.get(name='testFreezer01')
    storageinstance_instance.rack = 'NoMoreRack'
    storageinstance_instance.box = box
    storageinstance_instance.cell = cell
    storageinstance_instance.label = label
    storageinstance_instance.date_stored = date_stored
    print(stored_by_list)
    storageinstance_instance.stored_by = Author.objects.get(firstname=stored_by_list[0], lastname=stored_by_list[1])
    storageinstance_instance.notebook_ref = notebook_ref
    storageinstance_instance.notes = notes
    # print(storageinstance_instance.material)
    # print(storageinstance_instance.storage)
    # print(storageinstance_instance.rack)
    # print(storageinstance_instance.box)
    # print(storageinstance_instance.cell)
    # print(storageinstance_instance.label)
    # print(storageinstance_instance.date_stored)
    # print(storageinstance_instance.stored_by)
    # print(storageinstance_instance.notebook_ref)
    # print(storageinstance_instance.notes)
    storageinstance_instance.save()
    print(uid)
    print("#####################")

