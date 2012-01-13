"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import pdb
from django.contrib.auth.models import User
from django.test import TestCase

from mezzanine.core.models import CONTENT_STATUS_DRAFT
from mezzanine.pages.models import RichTextPage

from widget.forms import WidgetOptionsForm
from widget.models import Widget
from widget.models import WidgetSlot
from widget.widget_pool import get_widget
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
        self._user = User.objects.create_superuser(username=self._username, \
                        password=self._password, email="example@example.com")

    def test_widget_creation(self):
        test_widget = Widget()
        test_widget.widget_class = 'TestWidget'
        test_widget.user_id = 1
        widget_class = get_widget(test_widget.widget_class)

        self.assertEqual(widget_class.Meta.name, "Test")

    def test_widget_options_form(self):

        form = WidgetOptionsForm("TestWidget")
        field_label = [f for f in form.fields]
        expected = ['name', 'option_Option 1',\
                 'option_Option 2', 'option_Option 3']

        self.assertEqual(field_label, expected)

    def test_widget_options_form_saving(self):
        pass

    def test_widget_renderer(self):
        #create page with widget slots
        page = RichTextPage.objects.create(title="testpage",
                                           status=CONTENT_STATUS_DRAFT)
        #create widget slot
        slot = "slot" 

        #create test widget
        test_widget = Widget()
        test_widget.widget_class = 'TestWidget'
        test_widget.page = page
        test_widget.user_id = 1
        test_widget.slot = slot
        test_widget.save()

        context = {}
        context["page"] = page
        context["request"] = {"user": self._user}
        #render widget, there should be only one widget i.e test_widget
        widgets = render_widgets_for_slot(slot, context)
        self.assertEqual(widgets[0]['widget'], test_widget)
        #check if rendered content is correct
        self.assertEqual(widgets[0]['content'], "Test Widget Rendered")
