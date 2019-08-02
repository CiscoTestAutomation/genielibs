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
__version__ = '19.7'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

from genie import abstract
abstract.declare_package(__name__)

# try to record usage statistics
#  - only internal cisco users will have stats.CesMonitor module
#  - below code does nothing for DevNet users -  we DO NOT track usage stats
#    for PyPI/public/customer users
try:
    # new internal cisco-only pkg since devnet release
    from ats.cisco.stats import CesMonitor
except Exception:
    try:
        # legacy pyats version, stats was inside utils module
        from ats.utils.stats import CesMonitor
    except Exception:
        CesMonitor = None

finally:
    if CesMonitor is not None:
        # CesMonitor exists -> this is an internal cisco user
        CesMonitor(action = __name__, application='Genie').post()
        CesMonitor(action = __name__, application='pyATS Packages').post()
