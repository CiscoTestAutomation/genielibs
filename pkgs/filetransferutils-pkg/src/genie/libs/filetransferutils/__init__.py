'''
Module:
    genie.libs.filetransferutils

Description:
	This is the library sub-component of Genie for `genie.libs.filetransferutils`.
    A utility package for file transfer to/from remote servers using different protocols
    (tftp/ftp/scp...etc.)

'''

__version__ = '24.4'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

from .fileutils import FileUtils
from .fileserver import FileServer
