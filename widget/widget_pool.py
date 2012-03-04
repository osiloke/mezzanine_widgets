from collections import defaultdict
from pprint import pprint
import traceback
import sys

from django.db.models import get_model
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured

from mezzanine.conf import settings
from mezzanine.pages.models import Page


class WidgetAlreadyRegistered(Exception):
    """
    An attempt was made to register a widget more
    than once.
    """


class WidgetNotFound(Exception):
    """
    The requested widget was not found
    """

class WidgetHasNoOptions(Exception):
    """
    The widget has not options
    """

page_widgets = {}


def register_widget(widget_class):
    """
    Registers a widget in the widget registry

    args:
        widget_class should sublass WidgetClassBase
    """

    from widget.models import WidgetClassBase
    if not issubclass(widget_class, WidgetClassBase):
            raise ImproperlyConfigured(
                "widget_class must be a subclass of WidgetClassBase, %r is not."
                % widget_class
            )
    name = widget_class.__name__.lower()
    if name in page_widgets:
        raise WidgetAlreadyRegistered(
            _('The widget %s has already been registered.') % widget_class)
    page_widgets[name] = widget_class
    
def get_widget(name):
    try:
        return page_widgets[name.lower()]
    except Exception:
        raise WidgetNotFound


def get_all_page_widgets():
    autodiscover()
    listes = ((w, page_widgets[w].Meta.name) for w in page_widgets)
    return listes

def get_widget_array():
    return [w for w in page_widgets]

def get_page_widgets_for_slot(widget):
    pass


def get_widget_options(type):
    try: 
        widget_class = get_widget(type)
        return widget_class.options
    except AttributeError:
        raise WidgetHasNoOptions(Exception)

LOADED = False


def autodiscover():
    """
    Taken from ``django.contrib.admin.autodiscover`` and used to run
    any calls to the ``register_widget`` function.
    """
    from django.utils.importlib import import_module
    global LOADED
    if LOADED:
        return
    LOADED = True
    for app in settings.INSTALLED_APPS:
        try:
            import_module("%s.page_widgets" % app)
        except ImportError, e:
            if "WidgetModel" in "%s" % e:
                traceback.print_exc(file=sys.stdout)
            pass
