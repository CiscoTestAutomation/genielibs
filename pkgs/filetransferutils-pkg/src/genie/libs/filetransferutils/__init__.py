'''
Module:
    genie.libs.filetransferutils

Description:
	This is the library sub-component of Genie for `genie.libs.filetransferutils`.
    A utility package for file transfer to/from remote servers using different protocols
    (tftp/ftp/scp...etc.)

'''

__version__ = '20.5'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

from .fileutils import FileUtils

# try to record usage statistics
#  - only internal cisco users will have stats.CesMonitor module
#  - below code does nothing for DevNet users -  we DO NOT track usage stats
#    for PyPI/public/customer users
try:
    # new internal cisco-only pkg since devnet release
    from pyats.cisco.stats import CesMonitor
except Exception:
    try:
        # legacy pyats version, stats was inside utils module
        from pyats.utils.stats import CesMonitor
    except Exception:
        CesMonitor = None

finally:
    if CesMonitor is not None:
        # CesMonitor exists -> this is an internal cisco user
        CesMonitor(action = __name__, application='Genie').post()
        CesMonitor(action = __name__, application='pyATS Packages').post()
