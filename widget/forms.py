from django import forms
from django.forms.widgets import HiddenInput

from widget.widget_pool import get_widget_options, WidgetHasNoOptions, get_all_page_widgets
from widget.models import WidgetOptionEntry, Widget

from mezzanine.pages.models import Page
from mezzanine.conf import settings

from uuid import uuid4

import option_fields


class WidgetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        restrict_list = kwargs.pop("restrict_list", settings.RESTRICTED_WIDGETS)
        super(WidgetForm, self).__init__(*args, **kwargs)
        try:
            user = self.initial["user"]
            if user.is_superuser:
                restrict_list = None
        except KeyError:
            pass

        self.uuid = str(uuid4())
        self.fields["page"].queryset = Page.objects.get_query_set()
        self.fields["widget_class"].choices = get_all_page_widgets(restrict_list)

    class Meta:
        model = Widget
        fields = ('widget_class', 'user', 'page', 'widgetslot')
        widgets = {
            'page': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'widgetslot': forms.HiddenInput()
        }


class WidgetOptionsForm(forms.Form):
    """
    Dynamically created form for displaying widget options
    defined in a widget class. Based on mezzanine forms
    """
    extra_js = []
    hasOptions = False

#    widget_class = forms.HiddenInput(choices=get_all_page_widgets(settings.RESTRICTED_WIDGETS))

    def __init__(self, widget_class, *args, **kwargs):
        """
        Dynamically add each of the form fields for the given form model
        instance and its related field model instances.
        """
        #get widget options from widget_class
        self.extra_js = []
        super(WidgetOptionsForm, self).__init__(*args, **kwargs)
        self.widget_class = widget_class
        try:
            self.form_fields = get_widget_options(widget_class)
        except WidgetHasNoOptions:
            return None

        if self.form_fields:
            self.hasOptions = True
            for field in self.form_fields:
                field_key = "option_%s" % field.name
                field_class = option_fields.CLASSES[field.field_type]
                field_widget = option_fields.WIDGETS.get(field.field_type)
                field_args = {"label": field.name, "required": field.required,
                              "help_text": field.help_text}
                arg_names = field_class.__init__.im_func.func_code.co_varnames
                field_args.update(field.field_args)

                if "max_length" in arg_names:
                    field_args["max_length"] = settings.FORMS_FIELD_MAX_LENGTH
                if field_widget is not None:
                    field_args["widget"] = field_widget
                self.fields[field_key] = field_class(**field_args)
                css_class = field_class.__name__.lower()

                field_key_widget =  self.fields[field_key].widget
                if field.required:
                    css_class += " required"
                    if (settings.FORMS_USE_HTML5 and
                        field.field_type != option_fields.CHECKBOX_MULTIPLE):
                        field_key_widget.attrs["required"] = ""
                try:
                    field_key_widget.attrs["class"] = css_class + " " + field_key_widget.attrs["class"]
                except KeyError:
                    field_key_widget.attrs["class"] = css_class

                try:
                    self.extra_js.append("this.%s('%s');" % (field_key_widget.META.init_js, "id_%s" % field_key))
                except Exception:
                    pass

                try:
                    if field.placeholder_text and not field.default:
                        text = field.placeholder_text
                        self.fields[field_key].widget.attrs["placeholder"] = text
                except:
                    pass

    def save(self, widget=None, **kwargs):
        """
        Save all option ``WidgetOptionEntry`` with reference to the passed widget.
        """

        if self.hasOptions:
            for field in self.form_fields:
                field_key = "option_%s" % field.name
                value = self.cleaned_data[field_key]
                if isinstance(value, list):
                    value = ", ".join([v.strip() for v in value])
                if value:
                    option, created =  WidgetOptionEntry.objects.get_or_create(
                                        name=field.name, widget=widget, defaults={"value":value}
                    )
                    option.value = value
                    option.save()
        return True


def ModelFormForWidget(widget_model, fields=None, widget=None):
    meta_data = { "model": widget_model, }

    try:
        widget_overrides = settings.WIDGET_OVERRIDES
    except AttributeError:
        widget_overrides = {}

    if fields:
        meta_data.update({"fields": fields})

    if widget:
        widgets = {
            'widget': HiddenInput(),
            }
        meta_data.update({"widgets": widgets})

    meta = type('Meta', (), meta_data)

    class WidgetModelForm(forms.ModelForm):
        extra_js = []

        def __init__(self, *args, **kwargs):
            super(WidgetModelForm, self).__init__(*args, **kwargs)
            self.uuid = str(uuid4())
            for f in self.fields.keys():
                field_class = self.fields[f].__class__
                try:
                    field_type = widget_overrides[field_class]
                except KeyError:
                    pass
                else:
                    self.fields[f].widget = option_fields.WIDGETS[field_type]()
                css_class = self.fields[f].widget.attrs.get("class", "")
                css_class += " " + field_class.__name__.lower()
                self.fields[f].widget.attrs["class"] = css_class
                self.fields[f].widget.attrs["id"] = "%s" % (f)

                try:
                    self.extra_js.append("this.%s('%s');" % (self.fields[f].widget.META.init_js, "%s" % f))
                except Exception:
                    pass

    modelform_class = type('modelform', (WidgetModelForm,), {"Meta": meta})
    return modelform_class