from widget import widget_pool
from widget.models import WidgetOption as opt, WidgetClassBase

from django.utils.translation import ugettext_lazy as _


class BlogListWidget(WidgetClassBase):
    pass


class SocialLogosWidget(WidgetClassBase):
    template = "widgets/social.html"
default_placeholder = "left"

def render(self, context, slot, queryset):
    return context

class Meta:
    name = _("Social Logos")
    author = 'Progweb Team'


class SlideWidget(WidgetClassBase):
    "Displays a slideshow of a list of HtmlContents"
    model = HtmlContent
    template = "widgets/slide.html"
    default_placeholder = "middle"

    def render(self, context, slot, queryset=None, **kwargs):
        context.update({'query_set': queryset, 'model': self.model})
        return context

    class Meta:
        name = "Sliding Content"
        author = 'Progweb Team'

widget_pool.register_widget(SlideWidget)
widget_pool.register_widget(SocialLogosWidget)
