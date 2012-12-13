#!/usr/bin/env python
from setuptools import setup, find_packages

try:
    README = open('README.md').read()
except:
    README = None

try: 
    LICENSE = open('LICENSE.txt').read()
except: 
    LICENSE = None

setup(
    name = 'py-adyen',
    version = '0.1.6',
    description='Python/Django interface to the Adyen payment gateway.',
    long_description=README,
    author = 'Sander van de Graaf',
    author_email = 'mail@svdgraaf.nl',
    license = LICENSE,
    url = 'http://github.com/svdgraaf/py-adyen/',
    packages = find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
    ],
)
