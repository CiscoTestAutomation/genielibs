'''
    Module:
        libs.conf

    Description:
        This is the library sub-component of Genie for `genie.conf`. It Configures
        topology through Python object attributes, featuring a common object structure.
        These object's structures means that they are compatible with all operating
        systems and Management Interfaces (such as CLI/Yang/REST, etc.). These
        libraries are community driven.

'''

# metadata
__version__ = '21.12'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

from genie import abstract
abstract.declare_package(__name__)
