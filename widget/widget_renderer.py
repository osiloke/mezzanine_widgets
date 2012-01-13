
from widget.models import  Widget, WidgetModel
from widget.widget_pool import get_widget

from django.template.loader import render_to_string, get_template_from_string
from django.template import Template


def render_template(context, template, raw=False):
    """
    Renders any type of template, text or file or whatever
    """
    rendered = ''
    if raw:
        template = get_template_from_string(template)
        template.name = "custom_template"
        rendered = template.render(context)
    else:
        if isinstance(template, str):
            rendered = render_to_string(template, context)
        if isinstance(template, Template):
            rendered = template.render(context)
    return rendered


def render_widgets_for_slot(slot, widget_context):
    """
    Renders all widgets assigned to a WidgetSlot
    """

    page = widget_context.get("page", None)
    user = widget_context["request"].user
    #regular widgets
    slot_widgets = Widget.objects.published(user)\
                    .filter(widgetslot=slot,\
                        page=page, page_less=False)
    #Some widgets are not bound to one page, logo widget
    page_less_widgets = Widget.objects.published(user)\
                .filter(widgetslot=slot, page_less=True)
    rendered_widgets = []
    "Render regular paged widgets and page less widgets (universal widgets)"
    widgets = slot_widgets | page_less_widgets
    for widget in widgets:
        widget_class = get_widget(widget.widget_class)
        widget_context.update({'widget': widget})
        if widget_class is not None:
            widget_options = None
            widget_class = widget_class()
            if hasattr(widget_class, "options"):
                try:
                    widget_options = dict(((o["name"], o["value"])\
                         for o in widget.options.values("name", "value")))
                    widget_context.update({"opts": widget_options})
                except Exception, e:
                    raise e
            queryset = get_widget_model_queryset(widget, widget_class)
            rendered_widget = render_template(widget_class\
                    ._render(widget_context, slot, queryset, widget_options),\
                              widget_class.template, widget_class.raw)


            rendered_widgets.append({'widget': widget, \
                                    'meta': widget_class.Meta, \
                                    'content': rendered_widget})

    return rendered_widgets

def get_widget_model_queryset(widget, widget_class):
    try:
        if hasattr(widget_class, 'model'):
            'Widget class is associated with a model'
            model = widget_class.model
            if model and WidgetModel in (model.__bases__):
                'The widget model has to subclass the WidgetModel class'
                model_queryset = model.objects.filter(widget=widget)
                if len(model_queryset):
                    return model_queryset
    except Exception:
        raise
    return None
