from django.conf.urls import *

urlpatterns = patterns('',

    url(r'^organisms/list/$', 'materials.views.organisms_list'),
    url(r'^material/add/$', 'materials.views.material_add'),
    url(r'^material/list/$', 'materials.views.material_list'),

)