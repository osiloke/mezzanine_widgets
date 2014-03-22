import os
from widget.models import Widget
from widget.utilities import get_widget_model_queryset
from widget.widget_pool import get_widget

from django.template.loader import render_to_string, get_template_from_string
from django.template import Template


def render_template(context, template, raw=False):
    """
    Renders any type of template, text or file or whatever
    """
    rendered = ''
    if raw:
        template_object = get_template_from_string(template, name="custom_template_" + os.urandom(32))
        rendered = template_object.render(context)
    else:
        if isinstance(template, str):
            rendered = render_to_string(template, context)
        if isinstance(template, Template):
            rendered = template.render(context)
    return rendered


def make_or_get_widget_for_slot(slot, widget_context, widget_class, **kwargs):
    """
    Create or get a widget for a WidgetSlot
    Useful when creating templates and you want to add, for example, a default slidshow widget

    It only creates a new widget with the
    """
    page = widget_context.get("page", None)
    user = widget_context["request"].user

    widget_obj, created = Widget.objects.get_or_create(widgetslot=slot,
                                                       page=page, user=user,
                                                       widget_class=widget_class).defaults(**kwargs)

    return render_widget(widget_obj, widget_context)


def render_widget(widget, widget_context):
    """
    Render a single widgtet
    """
    widget_class = get_widget(widget.widget_class)
    widget_context.update({'widget': widget})

    if widget_class is not None:
        widget_options = None
        widget_class = widget_class()
        if hasattr(widget_class, "options"):
            try:
                widget_options = dict(((o["name"], o["value"]), for o in widget.options.values("name", "value")))
                widget_context.update({"opts": widget_options})
            except Exception, e:
                raise e
        queryset = get_widget_model_queryset(widget, widget_class)
        rendered_widget = render_template(widget_class._render(widget_context, widget.slot, queryset, widget_options),
                                          widget_class.template, raw=widget_class.raw)

        return {'widget': widget, 'meta': widget_class.Meta, 'content': rendered_widget}


def render_widgets_for_slot(slot, widget_context):
    """
    Renders all widgets assigned to a WidgetSlot
    """

    page = widget_context.get("page", None)
    user = widget_context["request"].user
    rendered_widgets = []
    "Render regular paged widgets and page less widgets (universal widgets)"
    widgets = Widget.objects.published_for_page_or_pageless(page, slot, user)
    for widget in widgets:
        widget_class = get_widget(widget.widget_class)
        widget_context.update({'widget': widget})
        if widget_class is not None:
            widget_options = None
            widget_class = widget_class()
            if hasattr(widget_class, "options"):
                try:
                    widget_options = dict(((o["name"], o["value"]), for o in widget.options.values("name", "value")))
                    widget_context.update({"opts": widget_options})
                except Exception, e:
                    raise e
            queryset = get_widget_model_queryset(widget, widget_class)
            rendered_widget = render_template(widget_class._render(widget_context, slot, queryset, widget_options),
                                              widget_class.template, raw=widget_class.raw)

            rendered_widgets.append({'widget': widget, 'meta': widget_class.Meta, 'content': rendered_widget})

    return rendered_widgets
