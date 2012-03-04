from django.utils.translation import ugettext_lazy as _

from widget import widget_pool
from widget.models import WidgetClassBase, WidgetOption as opt

from models import HtmlContent


class BlogListWidget(WidgetClassBase):
    template = "widgets/blogspot.html"

    def render(self, context, slot, queryset, **kwargs):
        return context

    class Meta:
        name = _("Blog Post List")
        author = 'Progweb Team'


class SocialLogosWidget(WidgetClassBase):
    template = "widgets/social.html"

    def render(self, context, slot, queryset, **kwargs):
        return context

    class Meta:
        name = _("Social Logos")
        author = 'Progweb Team'


class SlideWidget(WidgetClassBase):
    "Displays a slideshow of a list of HtmlContents"
    model = HtmlContent
    template = "widgets/slide.html"

    def render(self, context, slot, queryset=None, **kwargs):
        context.update({'query_set': queryset, 'model': self.model})
        return context

    class Meta:
        name = "Sliding Content"
        author = 'Progweb Team'


class TwitterMentionsWidgets(WidgetClassBase):
    "Displays recent messages for a twitter account, Uses"
    template = "widgets/twitter_mentions.html"

    options = [
        opt(name="Tag"),
    ]

    def render(self, context, **kwargs):
        return context

    class Meta:
        name = "Twitter Mentions"
        author = 'Progweb Team'


widget_pool.register_widget(BlogListWidget)
widget_pool.register_widget(SlideWidget)
widget_pool.register_widget(SocialLogosWidget)
widget_pool.register_widget(TwitterMentionsWidgets)
