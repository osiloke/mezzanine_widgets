from django.contrib.admin import TabularInline
from mezzanine.core.admin import OwnableAdmin, TabularDynamicInlineAdmin
from widget.models import WidgetOptionEntry
from widget.models import Widget
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class OptionEntryAdmin(TabularDynamicInlineAdmin):
    model = WidgetOptionEntry


#OptionFormset = forms.modelformset_factory(WidgetOptionEntry)


class OptionsAdmin(TabularInline):
    template = "admin/widget/edit_inline/tabular.html"
    model = WidgetOptionEntry


class WidgetAdmin(OwnableAdmin):
    inlines = [OptionsAdmin,]
    list_display = ("display_title", "status", "widgetslot", "admin_link")
    list_display_links = ("display_title",)
    list_editable = ("status",)
    list_filter = ("status","widgetslot",)
    search_fields = ("display_title","widget_class",)
    date_hierarchy = "publish_date"
    radio_fields = {"status": admin.HORIZONTAL}
    fieldsets = (
        (None, {"fields": ["page","display_title", "status",
            ("publish_date", "expiry_date"), ]}),
        (_("Widget"), {"fields": ("widgetslot", "widget_class")}),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Set the ID of the parent page if passed in via querystring.
        """
        # Force parent to be saved to trigger handling of ordering and slugs.
        parent = request.GET.get("widgetslot")
        if parent is not None and not change:
#            obj.widgetslot_id = parent
            obj._order = None
            obj.slug = None
            obj.save() 
        super(WidgetAdmin, self).save_model(request, obj, form, change)

admin.site.register(Widget, WidgetAdmin)
