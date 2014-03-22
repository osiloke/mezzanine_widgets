from widget.models import WidgetOption as opt, WidgetClassBase

from django.utils.translation import ugettext_lazy as _


class TestWidget(WidgetClassBase):
    template = "Test Widget Rendered"
    raw = True
    default_placeholder = "test"
    options = [
        opt(name="First"),
        opt(name="Second"),
        opt(name="Third")
    ]

    def render(self, context, slot, queryset=None, options=None, **kwargs):
        return context

    class Meta:
        hide = True
        page_less = True
        name = _("Test")
        author = 'Osiloke Emoekpere'
