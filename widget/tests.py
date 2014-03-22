"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import pdb
from django.contrib.auth.models import User
from django.template import RequestContext, Context
from django.test import TestCase

from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from mezzanine.pages.models import RichTextPage
from widget import widget_pool

from widget.forms import WidgetOptionsForm
from widget.models import Widget
from widget.page_widgets import TestWidget
from widget.widget_pool import get_widget, WidgetAlreadyRegistered
from widget.widget_renderer import render_widgets_for_slot


class Tests(TestCase):
    """
    Mezzanine Widget tests.
    """

    def setUp(self):
        """
        Create an admin user.
        """
        self._username = "test"
        self._password = "test"
        self._user = User.objects.create(username=self._username,
                                         password=self._password, email="example@example.com")

        #register our test widget
        try:
            widget_pool.register_widget(TestWidget)
        except WidgetAlreadyRegistered:
            pass

        #create page with widget slots
        self.page = RichTextPage.objects.create(title="testpage",
                                                status=CONTENT_STATUS_DRAFT)
        #create widget slot :)
        self.slot = "slot"

        #create test widget
        self.test_widgets = []
        self.widget_count = 3
        self.create_widgets()

    def create_widgets(self):
        for i in range(0, self.widget_count):
            test_widget = Widget()
            test_widget.widget_class = "TestWidget"
            test_widget.page = self.page
            test_widget.user_id = 1
            test_widget.widgetslot = self.slot
            test_widget.status = CONTENT_STATUS_DRAFT
            test_widget.save()
            self.test_widgets.append(test_widget)
        self.test_widgets[self.widget_count-1].status = CONTENT_STATUS_PUBLISHED
        self.test_widgets[self.widget_count-1].save()

    def test_widget_class(self):
        widget_class = get_widget(self.test_widgets[0].widget_class)
        self.assertEqual(widget_class.Meta.name, "Test")

    def test_widget_options_form_creation(self):
        form = WidgetOptionsForm("TestWidget")
        field_label = [f for f in form.fields]
        expected = ['option_First',
                    'option_Second', 'option_Third']

        self.assertListEqual(field_label, expected)

    def test_widget_options_form_saving(self):
        """
        This will modify a test widget with the assigned options
        """
        form = WidgetOptionsForm("TestWidget",
                                 data={
                                     "option_First": "Option 1",
                                     "option_Second": "Option 2",
                                     "option_Third": "Option 3"
                                 })
        self.assertEqual(form.is_valid(), True)

        form.save(self.test_widgets[0])

        self.assertListEqual([o.value for o in self.test_widgets[0].options.all()], ['Option 1', 'Option 2', 'Option 3'])

    def test_widget_renderer_for_page(self):

        #mock context
        context = {}
        context["page"] = self.page

        #mock request
        request = type('request', (object,), {'user': self._user})
        context["request"] = request

        #render widget, there should be only one widget i.e test_widget
        #This returns all widget's in the mentioned slot

        widgets = render_widgets_for_slot(self.slot, Context(context))

        #only one widget item is published
        self.assertEqual(len(widgets), 1)

        self.assertEqual(widgets[0]['widget'].status, CONTENT_STATUS_PUBLISHED)

        self.assertEqual(widgets[0]['widget'].display_title, self.test_widgets[self.widget_count-1].display_title)

        #check if rendered content is correct
        self.assertEqual(widgets[0]['content'], "Test Widget Rendered")
