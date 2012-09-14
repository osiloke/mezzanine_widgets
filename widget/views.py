from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from mezzanine.pages.models import Page
from mezzanine.template import get_template
from mezzanine.utils.views import is_editable
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED, CONTENT_STATUS_DRAFT

from widget.utilities import  LazyEncoder, ajax_view, get_model_form_for_widget, hasModel, get_widget_model_queryset
from widget.forms import WidgetForm, WidgetOptionsForm
from widget.widget_pool import  get_widget, WidgetHasNoOptions
from widget.utilities import admin_can
from widget.models import Widget
from widget.utilities import ajaxerror

json_serializer = LazyEncoder()

@login_required
@admin_can(Widget, action="change", fail404=True)
def edit_widget(request, **kwargs):
    try:

        widget = Widget.objects.get(id=kwargs.get("id"))
        widget_class_obj = get_widget(widget.widget_class)
        containsModel = hasModel(widget_class_obj)

        if request.POST:
            "get form populated with widget options"
            options_form = WidgetOptionsForm(widget.widget_class, \
                                request.POST)
            if options_form.is_valid():
                if options_form.save(widget=widget):
                    data = {'valid': True, 'form': 'saved'}
            elif options_form.errors:
                data = ajaxerror(options_form)
            if containsModel:
                obj = get_widget_model_queryset(widget, widget_class_obj)
                model_form = get_model_form_for_widget(widget_class_obj, \
                        {"POST":request.POST, "FILES":request.FILES}, instance=obj, widget=widget)
                try:
                    if model_form.is_valid():
                        saved_obj=model_form.save()
                        data.update({"obj": saved_obj.id})
                    elif model_form.errors:
                        model_data = ajaxerror(model_form)
                        errors = dict(data.get("errors", {}), **model_data["errors"])
                        data = {'valid': False, "errors": errors }
                except Exception:
                    raise
        else:
            "This is a request to get a form for widget"
            ctx = RequestContext(request)
            "get widget form populated with widget options"

            initial = {'status': widget.status}
            if widget.hasOptions:
                initial.update(dict(("option_%s" % option.name, option.value) \
                             for option in widget.options.all()))
            options_form = WidgetOptionsForm(widget.widget_class, \
                            data=initial)

            o = get_template("widget/options.html")
            ctx.update({'options_form': options_form})
            if containsModel:
                obj = get_widget_model_queryset(widget, widget_class_obj)
                model_form = get_model_form_for_widget(widget_class_obj, instance=obj, widget=widget)
                if model_form:
                    ctx.update({'model_form': model_form})

            options = o.render(ctx)

            extra_js = options_form.extra_js
            data = {'valid': False, 'type': 'ef', 'data': options, 'extra_js': extra_js}

        return HttpResponse(json_serializer.encode(data), \
                            mimetype='application/json')
    except Exception:
        raise


@login_required
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


            "Widget has options, lets generate the options form"
            options_form = WidgetOptionsForm(widget_class)
            if widget_form.is_valid():
                o = get_template("widget/options.html")
                ctx.update({'options_form': options_form,
                            'widget_class': widget_class_obj })
                model_form = get_model_form_for_widget(widget_class_obj)
                if model_form:
                    ctx.update({'model_form': model_form})

                options = o.render(ctx)
                data = {'valid': False, 'type':'fi', 'data':options}
            else:
                data = ajaxerror(widget_form)
            return HttpResponse(json_serializer.encode(data), mimetype='application/json')

        else:
            return HttpResponseRedirect("/")


@login_required
@admin_can(Widget, fail404=True)
def create_widget(request, **kwargs):
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
            widget_class_obj = get_widget(widget_class)
            containsModel = hasModel(widget_class_obj)

            slot = request.POST["widgetslot"]
            try:
                page = Page.objects.get(id=request.POST["page"])
                print page
                ### HANDLE OPTIONS FORM ####
                options_form = WidgetOptionsForm(widget_class, request.POST, request.FILES)
                widget = None
                if options_form.is_valid():
                    try:
                        "update widget if it exists"
                        widget = Widget.objects.get(id=request.POST["widget"])
                    except Exception:
                        widget = Widget(widgetslot=slot,
                                        widget_class=widget_class,
                                        user=request.user, page=page)
                        widget.save()

                    if options_form.save(widget=widget):
                        data = {'valid': True, 'form': 'saved'}
                elif options_form.errors:
                    data = ajaxerror(options_form)


                if widget is None and not options_form.hasOptions and containsModel:
                    try:
                        "update widget if it exists"
                        widget = Widget.objects.get(id=request.POST["widget"])
                    except Exception:
                        widget = Widget(widgetslot=slot,
                            widget_class=widget_class,
                            user=request.user, page=page)
                        widget.save()


                model_widget = None
                if widget: model_widget = widget
                model_form = get_model_form_for_widget(widget_class_obj, {"POST":request.POST, "FILES":request.FILES}, widget=model_widget)
                if model_form:
                    try:
                        if model_form.is_valid():
                            saved_obj=model_form.save()
                            data.update({"obj": saved_obj.id})
                        elif model_form.errors:
                            model_data = ajaxerror(model_form)
                            errors = dict(data.get("errors", {}), **model_data["errors"])
                            data = {'valid': False, "errors": errors }
                    except Exception:
                        raise
            except Exception, e:
                data = {"valid": False, "errors": { "_all_": ["Something went wrong, please refresh the page"], "exception": e.message}}

    return HttpResponse(json_serializer.encode(data),\
                                 mimetype='application/json')

create_widget = require_POST(create_widget)


@login_required
@admin_can(Widget, action="delete")
def delete_widget(request, id):

    data = {'valid': False}
    try:
        obj = Widget.objects.get(id=id)
        obj.delete()
        data = {'valid': True}
    except Exception:
        pass
    return HttpResponse(json_serializer.encode(data),\
        mimetype='application/json')

@login_required
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

@login_required
@admin_can(Widget)
def create_success(request):
    return render_to_response("widget/success.html", {})


#@ajax_view()
@admin_can(Widget, action="change")
def widget_ordering(request):
    """
    Based on mezzanine pages admin ordering
    Updates the ordering of widgets via AJAX from within the admin.
    """
    data = {"status": True}
    get_id = lambda s: s.split("_")[-1]
    for ordering in ("ordering_from", "ordering_to"):
        ordering = request.POST.get(ordering, "")
        if ordering:
            for i, widget in enumerate(ordering.split(",")):
                try:
                    Widget.objects.filter(id=get_id(widget)).update(_order=i)
                except Exception, e:
                    data = {'status':False, 'error':str(e)}
    try:
        moved_widget = int(get_id(request.POST.get("moved_widget", "")))
    except ValueError, e:
        pass
    else:
        moved_parent = request.POST.get("moved_parent", "")
        if not moved_parent:
            moved_parent = None
        try:
            widget = Widget.objects.get(id=moved_widget)
            widget.widgetslot = moved_parent
            widget.save()
        except Exception, e:
            data = {'status':False, 'error':str(e)}
    return HttpResponse(json_serializer.encode(data),\
        mimetype='application/json')


@login_required
@require_http_methods(["POST"])
@admin_can(Widget, action="change")
def widget_status(request):
    try:
        id = request.POST["id"]
        widget = Widget.objects.get(id=id)
        if widget.status is CONTENT_STATUS_DRAFT:
            widget.status = CONTENT_STATUS_PUBLISHED
        else:
            widget.status = CONTENT_STATUS_DRAFT
        widget.save()
        data = {"status":True, "published": widget.status}
    except Exception, e:
        data = {"status":False, "error": str(e.message)}

    return HttpResponse(json_serializer.encode(data),\
        mimetype='application/json')

