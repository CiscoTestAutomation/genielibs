#! /bin/env python

'''Setup file for libs.sdk

See:
    https://packaging.python.org/en/latest/distributing.html
'''

from ciscodistutils import setup, find_packages, is_devnet_build
from ciscodistutils.tools import (read,
                                  version_info,
                                  generate_cython_modules)

_INTERNAL_SUPPORT = 'pyats-support@cisco.com'
_EXTERNAL_SUPPORT = 'pyats-support-ext@cisco.com'

_INTERNAL_LICENSE = 'Cisco Systems, Inc. Cisco Confidential',
_EXTERNAL_LICENSE = 'Apache 2.0'

_INTERNAL_URL = 'http://wwwin-genie.cisco.com/'
_EXTERNAL_URL = 'https://developer.cisco.com/site/pyats/'


# pyats support mailer
SUPPORT = _EXTERNAL_SUPPORT if is_devnet_build() else _INTERNAL_SUPPORT

# license statement
LICENSE = _EXTERNAL_LICENSE if is_devnet_build() else _INTERNAL_LICENSE

# project url
URL = _EXTERNAL_URL if is_devnet_build() else _INTERNAL_URL

# compute version range
version, version_range = version_info('src', 'genie', 'libs', 'sdk', '__init__.py')

install_requires = []

import os
import sys

from setuptools.command.develop import develop as setupdevelop


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
    url = URL,

    # author details
    author = 'Cisco Systems Inc.',
    author_email = SUPPORT,

    # project licensing
    license = LICENSE,

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
