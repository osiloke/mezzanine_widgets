
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.base import Template
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.models import Page
from mezzanine.template import get_template
from mezzanine.utils.views import is_editable

from widget.utilities import  LazyEncoder, ajax_view
from widget.forms import WidgetForm, WidgetOptionsForm
from widget.widget_pool import get_all_page_widgets, get_widget, WidgetHasNoOptions
from widget.utilities import admin_can
from widget.models import Widget
from widget.utilities import ajaxerror

json_serializer = LazyEncoder()


def get_widget_list_for_page(page):
    try:
        all_classes = get_all_page_widgets()
        list = Template('widget/list.html')
        c = {'widgets': all_classes, 'page_id': page.id}

        return c
    except Exception:
        return None


@admin_can(Widget)
def edit_widget(request, widget):
    "Generate a form autopopulated with widget option data"
    if not is_editable(Widget(), request):
        response = _("Permission denied")
        data = {
            'error': [response],
            'permission': False
        }
    else:
        try:
            if request.POST:
                "get form populated with widget options"
                widget = Widget.objects.get(id=request.POST["widget"])
                options_form = WidgetOptionsForm(widget.widget_class, \
                                    request.POST)
                if options_form.is_valid():
                    if options_form.save(widget=widget):
                        data = {'valid': True, 'form': 'saved'}
                elif options_form.errors:
                    data = ajaxerror(options_form)
            elif request.GET:
                "This is a request to get a form for widget"
                ctx = RequestContext(request)
                "get widget form populated with widget options"
                if request.GET["widget"]:
                    widget = Widget.objects.get(id=request.GET["id"])
                    options = widget.options
                    initial = dict(("option_%s" % k, v) \
                                 for (k, v) in options.iteritems())
                    options_form = WidgetOptionsForm(widget.widget_class, \
                                    data=initial)

                elif request.GET["widget_class"]:
                    options_form = WidgetOptionsForm(request.GET["type"])

                o = get_template("widget/options.html")
                ctx.update({'options_form': options_form})

                options = o.render(ctx)
                data = {'valid': False, 'type': 'nf', 'data': options}
        except Exception:
            raise
        return HttpResponse(json_serializer.encode(data), \
                            mimetype='application/json')


@admin_can(Widget)
def widget_list(request):
    """
    Renders widget options based on supplied widget
    class or displays a select screen
    """
    data = {}
    if not is_editable(Widget(), request):
        response = _("Permission denied")
        data = {
            'error': [response],
            'permission': False
        }
    else:
        if request.POST:
            "widget class exists so render widget options if any"
            ctx = RequestContext(request)
            widget_form = WidgetForm(request.POST)
            widget_class = request.POST["widget_class"]
            widget_class_obj = get_widget(widget_class)

#            if hasattr(widget_class_obj, "options"):
            "Widget has options, lets generate the options form"
            options_form = WidgetOptionsForm(widget_class)
            if widget_form.is_valid():
                o = get_template("widget/options.html")
                ctx.update({'options_form': options_form,
                            'widget_class': widget_class_obj })

                options = o.render(ctx)
                data = {'valid': False, 'type':'fi', 'data':options}
            else:
                data = ajaxerror(widget_form)
            return HttpResponse(json_serializer.encode(data), mimetype='application/json')

        else:
            return HttpResponseRedirect("/")


@admin_can(Widget, fail404=True)
def create_widget(request):
    """
    Renders widget options based on supplied widget
    class or displays a select screen
    """
    data = {}
    if not is_editable(Widget(), request):
        response = _("Permission denied")
        data = {
            'error': {"_all_": [response]},
            'permission': False
        }
    else:
        if request.POST:
            widget_class = request.POST["widget_class"]
            slot = request.POST["widgetslot"]
            try:
                page_obj = Page.objects.published(request.user)\
                                .get(id=request.POST["page"])
                options_form = WidgetOptionsForm(widget_class, request.POST)
                if options_form.is_valid():
                    try:
                        "update widget if it exists"
                        widget = Widget.objects.get(id=request.POST["widget"])
                    except Exception:
                        widget = Widget(widgetslot=slot, page=page_obj,
                                        widget_class=widget_class,
                                        user=request.user)
                        widget.save()

                    if options_form.save(widget=widget):
                        data = {'valid': True, 'form': 'saved'}
                elif options_form.errors:
                    data = ajaxerror(options_form)
            except Exception, e:
                data = {"valid": "false", "error": { "_all_": ["Something went wrong, please refresh the page"],}}

    return HttpResponse(json_serializer.encode(data),\
                                 mimetype='application/json')

create_widget = require_POST(create_widget)


@admin_can(Widget, action="change")
def delete_widget(request, widget):
    try:
        obj = Widget.objects.get(id=widget)
        obj.delete()
    except Exception:
        pass


@ajax_view()
@admin_can(Widget)
def widget_options(request, type):
    try:
        options_form = WidgetOptionsForm(type)
        ctx = RequestContext(request)
        o = get_template("widget/options.html")
        ctx.update({'options_form': options_form,
                    'widget_class': options_form.widget_class })

        options = o.render(ctx)
        data = {'valid': True, 'type': 'fi', 'opts': options}
    except WidgetHasNoOptions:
        data = {"valid": False, "error": "None"}

    return data


@admin_can(Widget)
def create_success(request):
    return render_to_response("widget/success.html", {})
