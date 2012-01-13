from django.conf.urls.defaults import *
 

urlpatterns = patterns('widget.views',
    url(r'^create/$', "create_widget", name="create_widget"),
    url(r'^list/$', "widget_list", name="widget_list"),
    url(r'^success/$', "create_success", name="create_success"),
    url(r'^edit/(?P<widget>[\w]+)/$', "edit_widget", name="edit_widget"),
)