from __future__ import with_statement

import os
import sys
from setuptools import setup, find_packages 


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
    version='0.1.0dev',
    url='http://osiloke.blogspot.com',
    license='BSD',
    description="Makes it super easy to add extra content to mezzanine pages and also add extended functionality. Check out the example app.",
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=('example',)),
    install_requires=[
                "django >= 1.3",
                "mezzanine",
                "django-classy-tags", 
            ],
    classifiers=CLASSIFIERS,
)