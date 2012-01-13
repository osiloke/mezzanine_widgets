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
    version='0.0.9dev',
    url='http://osiloke.com',
    license='BSD',
    description="An app which makes it possible to create and add widgets to mezzanine pages.",
    long_description=open('README.txt').read(),
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(), 
    install_requires=[
                "django >= 1.3",
                "mezzanine",
                "django-classy-tags", 
            ],
    classifiers=CLASSIFIERS,
)