#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for Dirus.

Source:: https://github.com/ampledata/dirus
"""

import setuptools
import sys

__title__ = 'dirus'
__version__ = '0.0.1b1'
__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setuptools.setup(
    author='Greg Albrecht',
    author_email='oss@undef.net',
    description='Dirus',
    entry_points={
        'console_scripts': [
            'dirus = dirus.cmd:cli'
        ]
    },
    include_package_data=True,
    install_requires=['aprs'],
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    name='dirus',
    package_data={'': ['LICENSE']},
    package_dir={'dirus': 'dirus'},
    packages=['dirus'],
    url='http://github.com/ampledata/dirus',
    version=__version__,
    zip_safe=False
)
