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

args = argparse()
legacyDataSheet = args.legacyDataSheet

workbook = xlrd.open_workbook(legacyDataSheet)
datatab = workbook.sheet_by_index(0)

for row_index in range(2, datatab.nrows):
    row_content = datatab.row(row_index)
    print(row_content)
    [uid, organism, genotype, name, volume, concentration, quantity, box, cell, protocol, stored_by, date_stored, notebook_ref] = [
        int(row_content[0].value), row_content[1].value.rstrip(), row_content[2].value.rstrip(),
        str(row_content[3].value).rstrip(), row_content[4].value, row_content[5].value, row_content[6].value,
        row_content[7].value.rstrip(), row_content[8].value.rstrip(), row_content[9].value, row_content[10].value,
        row_content[11].value, row_content[12].value.rstrip()]
    print(uid)
    code = 'gDNA'+ format(uid, '04d')
    #material_properties = list(zip(['plasmid_or_glycerol', 'vector', 'resistance_marker', 'bacterial_strain', 'sequence'], [row_content[1].value.rstrip(), row_content[5].value.rstrip(), row_content[6].value.rstrip(), row_content[7].value.rstrip(), row_content[13].value.rstrip()]))
    material_properties = []
    # Parse author
    stored_by_list = []
    if stored_by == '':
        stored_by_list = ['Unknown', 'Unknown']
    elif stored_by == 'Genscript':
        stored_by_list = ['Genscript', 'Genscript']
    else:
        stored_by_list = stored_by.split(" ")

    #parse date
    if (date_stored == 'Blank') | (date_stored == ''):
        date_stored = '1000-01-01'
    else:
        date_stored = excelDateValue2timeStampStr(date_stored, outFormat='%Y-%m-%d')
    print(date_stored)
    orgdic = {'NA': 100, 'L. donovani 1S':5, 'L. tarentolae TarII': 6, 'L. major Friedlin': 1, 'T. cruzi YC': 10, 'T. cruzi CR Brener': 11, 'L. braziliensis M2904': 8, 'T. brucei 927': 9, 'L. donovani Bob': 7}
    genotypeObj = Genotype.objects.get(genotype='NA')
    organismObj = Organism.objects.get(id=orgdic[organism])
    typeObj = MaterialType.objects.get(type="GenomicDNA")
    protocolObj = Protocol.objects.get(name='test')

    material_instance = Material(genotype=genotypeObj, organism=organismObj, type=typeObj, protocol=protocolObj)
    material_instance.code = code
    material_instance.name = name
    material_instance.save()

    # Now save material properties
    for pair in material_properties:
        print(pair)
        materialproperty_instance = MaterialProperty(material=material_instance)
        materialproperty_instance.material_property_type = MaterialPropertyType.objects.get(term=pair[0])
        materialproperty_instance.value = pair[1]
        if pair[1] != '':
            materialproperty_instance.save()

    # Now save storage instance
    storageinstance_instance = StorageInstance(material=material_instance)
    storageinstance_instance.storage = Storage.objects.get(name='testFreezer02')
    storageinstance_instance.rack = 'NoMoreRack'
    storageinstance_instance.box = box
    storageinstance_instance.cell = cell
    #storageinstance_instance.label = label
    storageinstance_instance.date_stored = date_stored
    print(stored_by_list)
    storageinstance_instance.stored_by = Author.objects.get(firstname=stored_by_list[0], lastname=stored_by_list[1])
    storageinstance_instance.notebook_ref = notebook_ref
    storageinstance_instance.save()
    print(uid)
    print("#####################")

