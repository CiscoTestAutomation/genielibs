#! /usr/bin/env python
'''Setup file for libs.health Namespace Package

See:
    https://packaging.python.org/en/latest/distributing.html
'''

import re
import os

from setuptools import setup, find_packages


def read(*paths):
    '''read and return txt content of file'''
    with open(os.path.join(os.path.dirname(__file__), *paths)) as fp:
        return fp.read()


def find_version(*paths):
    '''reads a file and returns the defined __version__ value'''
    version_match = re.search(r"^__version__ ?= ?['\"]([^'\"]*)['\"]",
                              read(*paths), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = ['setuptools', 'wheel', 'genie']

# launch setup
setup(
    name='genie.libs.health',
    version=find_version('src', 'genie', 'libs', 'health', '__init__.py'),

    # descriptions
    description='pyATS Health Check for monitoring device health status',
    long_description=read('DESCRIPTION.rst'),

    # the project's main homepage.
    url='https://developer.cisco.com/pyats',

    # author details
    author='Cisco Systems Inc.',
    author_email='pyats-support-ext@cisco.com',

    # project licensing
    license='Apache 2.0',

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 6 - Mature',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # project keywords
    keywords='genie health pyats cisco',

    # project directory
    package_dir={
        '': 'src',
    },

    # project packages
    packages=find_packages(where='src'),

    # additional package data files that goes into the package itself
    package_data={
        '': ['health_yamls/*.yaml',
             '*.json'],
    },

    # console entry point
    entry_points={
        'pyats.easypy.plugins':
        ['plugin = genie.libs.health.plugin:health_plugin']
    },

    # package dependencies
    install_requires=install_requires,

    # any additional groups of dependencies.
    # install using: $ pip install -e .[dev]
    extras_require={
        'dev': [
            'coverage', 'paramiko', 'restview', 'Sphinx', 'sphinx-rtd-theme',
            'sphinxcontrib-mockautodoc'
        ],
    },

    # external modules
    ext_modules=[],

    # any data files placed outside this package.
    # See: http://docs.python.org/3.5/distutils/setupscript.html
    # format:
    #   [('target', ['list', 'of', 'files'])]
    # where target is sys.prefix/<target>
    data_files=[],

    # non zip-safe (never tested it)
    zip_safe=False,
)