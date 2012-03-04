NOTE:
=========
This app was pulled out of an existing project i have, and as a result some features may not work yet (e.g Frontend widget adding).

OVERVIEW
=========
This app extends mezzanine applications by provides an interface for adding dynamic custom content like a twitter mentions widget,
custom text, custom html to mezzanine pages without modifying templates or implementing a full django app.

Requirements
============
mezzanine 1.0
django-classy-tags

METHODOLOGY
===========

Widgets are placed in the specified slot. Slots are just placeholders inside django templates where widgets are rendered.
They are not stored in the database. As a result, a template designer does not worry about syncing the database
every time he wants to create a `slot` in a template. On the other hand, the end user must be aware of the `slots` available for
widgets.

Widget Classes contain the logic used to render each widget and are dynamically loaded at runtime using the same autoloading logic
used for django admin.

USAGE
=====

Page Widgets
------------
The widget app searches all apps in loaded in django for a file named `page_widgets.py`. This file contains code which describe
how a widget should be rendered. An example widget which displays the addthis links is shown below::

    class SocialLogosWidget(WidgetClassBase):
        template = "widgets/social.html"

        def render(self, context, slot, queryset, **kwargs):
            return context

        class Meta:
            name = _("Social Logos")
            author = 'Progweb Team'

This widget just renders the social.html template which contains the addthis links.

Widgets can also have options. A widget which shows mentions of a twitter user is shown below::

    class TwitterMentionsWidgets(WidgetClassBase):
        "Displays recent messages for a twitter account, Uses"
        template = "widgets/twitter_mentions.html"

        options = [
            opt(name="Tag"), #The twitter tag to list
        ]
        class Meta:
            name = "Twitter Mentions"
            author = 'Progweb Team'


Rendering
---------
Render widgets on a page by first including the widget tag library.

	{% load widget_tags %}

You will need to load the javascript code which is used to manipulate widgets. The following should go in your base template.

    {% widget_loader %}

The following snippet will render widgets which are assigned to the footer slot.

	{% render_widgets "footer" %}

TODO
====
* Allow widgets to be assigned to slots from frontend (Currently porting code from my other project).
  This would eliminate the need to go through the backend.