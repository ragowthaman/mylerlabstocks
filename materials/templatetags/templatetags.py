from django import template

register = template.Library()




def hash(h,key):
    print(h)
    print(key)
    if key in h:
        print(h[key])
        return h[key]
    else:
        return None

register.filter(hash)

def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

register.filter(addstr)

def material_fields_to_display(object, fieldname):
    return object.material.fieldname

register.filter(material_fields_to_display)
