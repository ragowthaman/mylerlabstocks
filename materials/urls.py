from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^list/organisms/$', 'materials.views.list_organisms'),
    url(r'^add/materials/$', 'materials.views.add_material'),
    url(r'^list/materials/$', 'materials.views.list_materials'),
    url(r'^list/storages/$', 'materials.views.list_storages'),
    url(r'^list/racks/(?P<storage_unit_id>.+)/$', 'materials.views.list_racks'),
    url(r'^list/boxes/(?P<storage_unit_id>.+)/(?P<rack_name>.+)/$', 'materials.views.list_boxes'),
    url(r'^view/box/listview/(?P<storage_unit_id>.+)/(?P<rack_name>.+)/(?P<box_name>.+)/$', 'materials.views.viewbox_listview'),
    url(r'^view/box/boxview/(?P<storage_unit_id>.+)/(?P<rack_name>.+)/(?P<box_name>.+)/$', 'materials.views.viewbox_boxview'),

)