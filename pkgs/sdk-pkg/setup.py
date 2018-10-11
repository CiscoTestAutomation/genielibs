#! /usr/bin/env python

'''Setup file for libs.sdk

See:
    https://packaging.python.org/en/latest/distributing.html
'''

import os
import sys
import re

from setuptools import setup, find_packages
from setuptools.command.develop import develop as setupdevelop

def read(*paths):
    '''read and return txt content of file'''
    with open(os.path.join(*paths)) as fp:
        return fp.read()


def find_version(*paths):
    '''reads a file and returns the defined __version__ value'''
    version_match = re.search(r"^__version__ ?= ?['\"]([^'\"]*)['\"]",
                              read(*paths), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# compute version range
version = find_version('src', 'genie', 'libs', 'sdk', '__init__.py')

install_requires = []

class DevelopCommand(setupdevelop):
    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

        src = os.path.abspath('genie_yamls')
        dst = os.path.join(sys.prefix, 'genie_yamls')

        if self.uninstall is None:
            # If directory/symlink already exists, then error out
            if os.path.lexists(dst):
                raise Exception("'{dst}' already exists, delete/move it".format(dst=dst))

            print('Creating symbolic link at from {src} to {dst}'.format(src=src, dst=dst))
            os.symlink(src, dst)
        else:
            if os.path.lexists(dst):
                print('Removing symbolic link {dst}'.format(dst=dst))
                os.unlink(dst)

def find_yamls(*paths):
    '''finds all genie_yamls'''
    files = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(*paths)):
        files.append((dirpath, [os.path.join(dirpath, f) for f in filenames]))

    return files

# launch setup
setup(

    # update commands list with default options
    # and apply user's options on top
    cmdclass={'develop':DevelopCommand},

    name = 'genie.libs.sdk',
    version = version,

    # descriptions
    description = 'Genie libs sdk: Libraries containing all Triggers and Verifications',
    long_description = read('DESCRIPTION.rst'),

    # the project's main homepage.
    url = 'https://developer.cisco.com/site/pyats/',

    # author details
    author = 'Cisco Systems Inc.',
    author_email = 'pyats-support-ext@cisco.com',

    # project licensing
    license = 'Apache 2.0',

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # project keywords
    keywords = 'genie pyats test automation',

    # uses namespace package
    namespace_packages = ['genie', 'genie.libs'],

    # project packages
    packages = find_packages(where = 'src'),

    # project directory
    package_dir = {
        '': 'src',
    },

    # additional package data files that goes into the package itself
    package_data = {
    },

    # console entry point
    entry_points = {
    },

    # package dependencies
    install_requires = install_requires,

    # any additional groups of dependencies.
    # install using: $ pip install -e .[dev]
    extras_require = {
        'dev': ['coverage',
                'restview',
                'Sphinx',
                'sphinxcontrib-napoleon',
                'sphinx-rtd-theme'],
    },

    # external modules
    ext_modules = [],

    # any data files placed outside this package.
    # See: http://docs.python.org/3.4/distutils/setupscript.html
    # format:
    #   [('target', ['list', 'of', 'files'])]
    # where target is sys.prefix/<target>
    data_files = find_yamls('genie_yamls'),

    # non zip-safe (never tested it)
    zip_safe = False,
)
