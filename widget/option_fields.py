
from django import forms
from django.forms.extras import SelectDateWidget
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.forms import SplitSelectDateTimeWidget


# Constants for all available field types.
from mezzanine.utils.importing import import_dotted_path

TEXT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX = 4
CHECKBOX_MULTIPLE = 5
SELECT = 6
SELECT_MULTIPLE = 7
RADIO_MULTIPLE = 8
FILE = 9
DATE = 10
DATE_TIME = 11
HIDDEN = 12
NUMBER = 13
URL = 14
RICHTEXTAREA = 15
IMAGE = 16
# Names for all available field types.
NAMES = (
    (TEXT, _("Single line text")),
    (TEXTAREA, _("Multi line text")),
    (EMAIL, _("Email")),
    (NUMBER, _("Number")),
    (URL, _("URL")),
    (CHECKBOX, _("Check box")),
    (CHECKBOX_MULTIPLE, _("Check boxes")),
    (SELECT, _("Drop down")),
    (SELECT_MULTIPLE, _("Multi select")),
    (RADIO_MULTIPLE, _("Radio buttons")),
    (FILE, _("File upload")),
    (DATE, _("Date")),
    (DATE_TIME, _("Date/time")),
    (HIDDEN, _("Hidden")),
    (RICHTEXTAREA, _("Multi line text")),
    (IMAGE, _("Image")),
    )

# Field classes for all available field types.
CLASSES = {
    TEXT: forms.CharField,
    TEXTAREA: forms.CharField,
    RICHTEXTAREA: forms.CharField,
    EMAIL: forms.EmailField,
    CHECKBOX: forms.BooleanField,
    CHECKBOX_MULTIPLE: forms.MultipleChoiceField,
    SELECT: forms.ChoiceField,
    SELECT_MULTIPLE: forms.MultipleChoiceField,
    RADIO_MULTIPLE: forms.ChoiceField,
    FILE: forms.FileField,
    DATE: forms.DateField,
    DATE_TIME: forms.DateTimeField,
    HIDDEN: forms.CharField,
    NUMBER: forms.FloatField,
    URL: forms.URLField,
    IMAGE: forms.ImageField,
    }

# Widgets for field types where a specialised widget is required.
WIDGETS = {
    TEXTAREA: forms.Textarea,
    RICHTEXTAREA: import_dotted_path(settings.RICHTEXT_WIDGET_CLASS),
    CHECKBOX_MULTIPLE: forms.CheckboxSelectMultiple,
    RADIO_MULTIPLE: forms.RadioSelect,
    DATE: SelectDateWidget,
    DATE_TIME: SplitSelectDateTimeWidget,
    HIDDEN: forms.HiddenInput,
    }

# Some helper groupings of field types.
CHOICES = (CHECKBOX, CHECKBOX_MULTIPLE, SELECT,
           SELECT_MULTIPLE, RADIO_MULTIPLE)
DATES = (DATE, DATE_TIME)
MULTIPLE = (CHECKBOX_MULTIPLE, SELECT_MULTIPLE)

# HTML5 Widgets
if settings.FORMS_USE_HTML5:
    html5_field = lambda name, base: type("", (base,), {"input_type": name})
    WIDGETS.update({
        DATE: html5_field("date", forms.DateInput),
        DATE_TIME: html5_field("datetime", forms.DateTimeInput),
        EMAIL: html5_field("email", forms.TextInput),
        NUMBER: html5_field("number", forms.TextInput),
        URL: html5_field("url", forms.TextInput),
        })
