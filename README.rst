OVERVIEW
=========
An app which makes it possible to create and add widgets to mezzanine pages. 
Widgets can be edited from the frontend using the mezzanine frontend app, which provides frontend add, edit and delete functions for any type of django model (to be released soon).
This app is based extensively on mezzanine and django-classy-tags.

METHODOLOGY
===========

Widgets can be placed in slots.
Slots are just tag names assigned at runtime from django templates. 
They are not stored in the database. As a result of this a template designer does not worry about syncing the database
everytime he wants to provision footer widgets.

Widget Classes contain the logic used to render each widget and are dynamically loaded at runtime using the same autoloading logic
used for django admin.

USAGE
========
Render widgets on a page by first including the widget tag library.
	{% load widget_tags %}

The following snippet will render tags which are assigned to the footer slot.

	{% render_widgets footer %}

Widgets can be added from the frontend (comming soon)