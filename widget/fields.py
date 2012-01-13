from django import forms
from django.db import models
from django.utils.encoding import smart_unicode


class PageWidgetClassField(forms.ChoiceField):
    """Renders a PageWidgetClass field with choices obtained
        from all the available widget classes
    """
    def __init__(self, *args, **kwargs):
        kwargs.pop('max_length', '')
        from widget.widget_pool import get_all_page_widgets
        super(PageWidgetClassField, self).__init__(*args, **kwargs)
        choices = get_all_page_widgets()
        self.choices = choices


class PageWidgetClass(models.CharField):
    description = "A field which holds the name of a widget \
                    class associated with a page widget"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        from widget.widget_pool import get_all_page_widgets
        kwargs['choices'] = get_all_page_widgets()
        super(PageWidgetClass, self).__init__(*args, **kwargs)

    def formfield(self, form_class=forms.CharField, **kwargs):
        # This is a fairly standard way to set up some defaults
#        while letting the caller override them.
        defaults = {'form_class': PageWidgetClassField}
#        if self.choices:
#            defaults = {'choices': self.choices}
#        else:
#            defaults = {'form_class': PageWidgetClassField}
        defaults.update(kwargs)
        return super(PageWidgetClass, self).formfield(**defaults)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        field_class = self.__class__.__module__ + "." + self.__class__.__name__
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

