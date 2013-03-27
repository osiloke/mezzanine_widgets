from django.conf.urls.defaults import *
 

urlpatterns = patterns('widget.views',
    url(r'^create/$', "create_widget", name="create_widget"),
    url(r'^list/$', "widget_list", name="widget_list"),
    url(r'^success/$', "create_success", name="create_success"),
    url(r'^edit/(?P<id>[\w]+)/$', "edit_widget", name="edit_widget"),
    url(r'^delete/(?P<id>[\w]+)/$', "delete_widget", name="delete_widget"),
    url(r'^options/(?P<type>[\w]+)/$', "widget_options", name="widget_options"),
    url(r'^order/$', "widget_ordering", name="widget_ordering"),
    url(r'^status/$', "widget_status", name="widget_status"),
)