'''
    Module:
        libs.robot

    Description:
        This is the library sub-component of Genie for `genie.robot`.

'''

# metadata
__version__ = '3.0.3'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

try:
    from ats.cisco.stats import CesMonitor
    CesMonitor(action = 'genielibsRobot', application='Genie').post()
except Exception:
    try:
        from ats.utils.stats import CesMonitor
        CesMonitor(action = 'genielibsRobot', application='Genie').post()
    except Exception:
        pass

from genie import abstract
abstract.declare_package(__name__)
