from __future__ import with_statement

import os
import sys
from setuptools import setup, find_packages 

def fullsplit(path, result=None):
    """
Split a pathname into components (the opposite of os.path.join) in a
platform-neutral way.
"""
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == "":
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)



package_dir = "widget"


packages = []

for dirpath, dirnames, filenames in os.walk(package_dir):
    # ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        packages.append(".".join(fullsplit(dirpath)))

template_patterns = [
    'templates/*.html',
    'templates/*/*.html',
    'templates/*/*/*.html',
    'templates/*/*/*/*.html',
    'static/widget/css/*',
    'static/widget/js/*'
]

static_patterns = [
    'static/*'
]

package_data = dict(
    (package_name, template_patterns)
    for package_name in packages
)



CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='Mezzanine Widgets',
    author='Osiloke Emoekpere',
    version='1.5.1',
    url='http://osiloke.blogspot.com',
    license='BSD',
    description="Makes it super easy to add extra content to mezzanine pages and also add extended functionality. Check out the example app.",
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,
    package_data=package_data,
    packages=packages,
    install_requires=[
                "django >= 1.3",
                "mezzanine",
                "django-classy-tags", 
            ],
    classifiers=CLASSIFIERS,
)
