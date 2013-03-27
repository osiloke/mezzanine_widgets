from mezzanine.conf import register_setting

from django.utils.translation import ugettext as _

#register_setting(
#    name="IMAGE_FIELD_WIDGET_CLASS",
#    description=_("Dotted package path and class name of the widget to use "
#                  "for the image fields`."),
#    editable=False,
#    default="django.forms.FileInput",
#)

register_setting(
    name="RESTRICTED_WIDGETS",
    label="Restricted Widgets",
    description=_("Widgets which cannot be added by a client "),
    editable=False,
    append=True,
    default=[
        "TestWidget"
    ],
)

register_setting(
    name="WIDGET_PERMISSION_HANDLER",
    label="Widget Permission Handler",
    description=_("A class which handles permissions for widgets"),
    editable=False,
    default=None,
)