from copy import copy
from django.http import HttpResponse
 

__author__ = 'osilocks'

from django.db.models.related import RelatedObject
from django.http import HttpResponseRedirect, Http404
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.db.models import get_model
from django.core.exceptions import ObjectDoesNotExist
import os, errno

try:
    from simplejson import JSONEncoder
except ImportError:
    try:
        from json import JSONEncoder
    except ImportError:
        from django.utils.simplejson import JSONEncoder

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

def check_permission(request, perm_name, app_label, model_name):
    '''
    Check for proper permissions. mode_name may be either add, change or delete.

    '''
    obj = model = get_model(app_label, model_name)
    if hasattr(obj, "is_%sable"% perm_name):
        return getattr(obj, "is_%sable"% perm_name)(request)
    else:
        p = '%s.%s_%s' % (app_label, perm_name, model_name)
        return request.user.is_active and request.user.has_perm(p)

def can(action, obj, request ):
    """
    Returns ``True`` if the user can execute the action for the object using the request.
    First check for a custom ``action`` handler on the object, otherwise use the logged
    in user and check action permissions for the object's model.
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.module_name

    if hasattr(obj, "is_%sable"% action):
        return getattr(obj, "is_%sable"% action)(request)
    else:
        p = '%s.%s_%s' % (app_label, action, model_name)
        return request.user.is_active and request.user.has_perm(p)
    return False

def model_to_dict(obj, exclude=['AutoField', 'ForeignKey', \
    'OneToOneField']):
    '''
        serialize model object to dict with related objects

        author: Vadym Zakovinko <vp@zakovinko.com>
        date: January 31, 2011
        http://djangosnippets.org/snippets/2342/
    '''
    tree = {}
    for field_name in obj._meta.get_all_field_names():
        try:
            field = getattr(obj, field_name)
        except (ObjectDoesNotExist, AttributeError):
            continue

        if field.__class__.__name__ in ['RelatedManager', 'ManyRelatedManager']:
            if field.model.__name__ in exclude:
                continue

            if field.__class__.__name__ == 'ManyRelatedManager':
                exclude.append(obj.__class__.__name__)
            subtree = []
            for related_obj in getattr(obj, field_name).all():
                value = model_to_dict(related_obj, \
                    exclude=exclude)
                if value:
                    subtree.append(value)
            if subtree:
                tree[field_name] = subtree

            continue

        field = obj._meta.get_field_by_name(field_name)[0]
        if field.__class__.__name__ in exclude:
            continue

        if field.__class__.__name__ == 'RelatedObject':
            exclude.append(field.model.__name__)
            tree[field_name] = model_to_dict(getattr(obj, field_name), \
                exclude=exclude)
            continue

        value = getattr(obj, field_name)
        if value:
            tree[field_name] = value

    return tree


def get_field_object_by_name(obj, field):
    """
    Searches through an objects field and returns the field object
    Finds any type of fields including related fields
    Args:
        obj (Model): The model which contains the field
        field (basestring): field
    """

    opts = obj._meta
    for f in opts.get_all_field_names():
        if f in field:
            field = opts.get_field_by_name(f)[0]
            return field
    return None


def checkObjectFields(obj, fields):
    """Validates field names against a django model
    Args:
        obj (Model): The model to check

        fields (array): The list of fields
    Return:
        array.
    """
    valid_fields = []
    opts = obj._meta
    for f in fields:
        try:
            'Check if the field name is an attribute only if it is a string'
            opts.get_field(f)
            valid_fields.append(f)
        except:
            pass
    return valid_fields


def mkdir_p(path):
    try:
        os.makedirs(path)
        return path
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


from functools import wraps
json_serializer = LazyEncoder()


def ajax_view():
    def _dec(view):
        def _view(request, *args, **kwargs):
            data = view(request, *args, **kwargs)
            return HttpResponse(json_serializer.encode(data),\
                    mimetype='application/json')
        _view.__name__ = view.__name__
        _view.__dict__ = view.__dict__
        _view.__doc__ = view.__doc__

        return wraps(view)(_view)
    return _dec

def admin_can(model, action="add", fail404=False):
    def _dec(view):
        def _view(request, *args, **kwargs):
            redirect_field_name = "next"
            url = None
            if redirect_field_name \
                and redirect_field_name in request.REQUEST:
                url = request.REQUEST[redirect_field_name]
            if not url:
                url = "/"
            if not can(action, model, request):
                if fail404:
                    raise Http404
                return HttpResponseRedirect(url)
            else:
                response = view(request, *args, **kwargs)
                if not type(response) is HttpResponse:
                    return HttpResponseRedirect(url)
                else:
                    return response

        _view.__name__ = view.__name__
        _view.__dict__ = view.__dict__
        _view.__doc__ = view.__doc__

        return wraps(view)(_view)
    return _dec

def ajaxerrors(forms):
    if isinstance(lst, basestring):
        for form in forms:
            ajaxerror(form)

def ajaxerror(form):
    "from django_ajax_validation"
    data = {}
    errors = copy(form.errors)
    formfields = dict([(fieldname, form[fieldname]) for fieldname in form.fields.keys()])
    final_errors = {}
    for key, val in errors.iteritems():
        if '__all__' in key:
            final_errors[key] = val
        else:# not isinstance(formfields[key].field):
            html_id = formfields[key].field.widget.attrs.get('id') or formfields[key].auto_id
            html_id = formfields[key].field.widget.id_for_label(html_id)
            final_errors[html_id] = val
    data.update({
        'valid': False,
        'errors': final_errors,
    })
    return data