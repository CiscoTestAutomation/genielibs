"""
Module:
    genie.libs.filetransferutils

Description:
        This is the library sub-component of Genie for `genie.libs.filetransferutils`.
    A utility package for file transfer to/from remote servers using different protocols
    (tftp/ftp/scp...etc.)

"""

__version__ = "26.4"
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

from genie import abstract

from .fileserver import FileServer
from .fileutils import FileUtils

ABSTRACT_ORDER = ["os", "protocol"]
abstract.declare_package(feature="filetransferutils", order=ABSTRACT_ORDER)
