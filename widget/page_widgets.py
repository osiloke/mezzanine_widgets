from widget import widget_pool
from widget.models import WidgetOption as opt, WidgetClassBase

from django.utils.translation import ugettext_lazy as _


class TestWidget(WidgetClassBase):
    template = "Test Widget Rendered"
    raw = True
    default_placeholder = "test"
    options = [
        opt(name="Option 1"),
        opt(name="Option 2"),
        opt(name="Option 3")
    ]

    def render(self, context, slot, queryset, **kwargs):
        return context

    class Meta:
        hide = True
        page_less = True
        name = _("Test")
        author = 'Osiloke Emoekpere'

#widget_pool.register_widget(TestWidget)
