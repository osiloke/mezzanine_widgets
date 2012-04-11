OVERVIEW
========= 
:Author: Osi Emoekpere (http://osiloke.blogspot.com, http://twitter.com/osilocks)

:info: This app extends mezzanine applications by provides an interface for adding dynamic custom content like a twitter mentions widget or slideshow to mezzanine pages.

Requirements
============
mezzanine 1.0 (I'm not sure if 1.0 is backwards compatible)
django-classy-tags

METHODOLOGY
===========
Widgets are placed in the specified slot. Slots are just placeholders inside django templates where widgets are rendered.
They are not stored in the database. As a result, a template designer does not worry about syncing the database
every time he wants to create a `slot` in a template. On the other hand, the end user must be aware of the `slots` available for
widgets.

Widget Classes contain the logic used to render each widget and are dynamically loaded at runtime using the same autoloading magic
used for django admin.

Setup
=====
Add the widget app to your installed apps after all mezzanine apps in your ``settings.py``::

   INSTALLED_APPS = (
       ...
       'widget',
       ...
   )

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
            opt(name="Tag", required=True, help_text="#Tag to list"),
            opt(name="Limit", default=3, help_text="Number of tweets to show"),
        ]

        def render(self, context, **kwargs):
            return context

        class Meta:
            name = "Twitter Mentions"
            author = 'Progweb Team'


Widgets are not used in the application until they are registered::

    widget_pool.register_widget(SocialLogosWidget)
    widget_pool.register_widget(TwitterMentionsWidgets)

The template variable can either be the path to a template file or a string with the template definition


Rendering
---------
Render widgets on a page by first including the widget tag library.::

	{% load widget_tags %}

You will need to load the javascript code which is used to manipulate widgets. The following should go in your base template.::

    {% widget_loader %}

The following snippet will render widgets which are assigned to the footer slot.::

	{% render_widgets "footer" %}


Adding Widgets
--------------
It is really easy to add widgets from the frontend site. Just look for the `Add Widget` link and click it. You will get a
list of widgets to choose from. If the widget has options, you will be able to enter them. Try adding the twitter mentions widget.

Example Project
===============
Install the widgets app by running::

python setup.py install #From the `widget` folder

Change directory to the example app and run::

python manage.py createdb --noinput

TODO
====
* Better presentation of widget list in frontend.
* Utilize more of bootstrap
* Fix edit widget function
* Sorting and swapping widgets
* More render options