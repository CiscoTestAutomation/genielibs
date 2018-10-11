'''
    Module:
        libs.ops

    Description:
        This is the library sub-component of Genie for `genie.ops`.
'''

# metadata
<<<<<<< HEAD
__version__ = '3.1.0'
=======
__version__ = '3.0.4'
>>>>>>> 52077bb96b9fe38662c5be4c54dd716ba29de872
__author__ = 'Cisco Systems Inc.'
__contact__ = ['pyats-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2018, Cisco Systems Inc.'

try:
    from ats.cisco.stats import CesMonitor
    CesMonitor(action = 'genielibsOps', application='Genie').post()
except Exception:
    try:
        from ats.utils.stats import CesMonitor
        CesMonitor(action = 'genielibsOps', application='Genie').post()
    except Exception:
        pass

from genie import abstract
abstract.declare_package(__name__)
