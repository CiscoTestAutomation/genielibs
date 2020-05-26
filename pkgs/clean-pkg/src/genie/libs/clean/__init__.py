'''
    Module:
        genie.libs.clean

    Description:
        This is the sub-component of Genie for `genie.libs.clean`.

'''

# metadata
__version__ = '20.5'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['asg-genie-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'


from genie import abstract
abstract.declare_package(__name__)


# try to record usage statistics
#  - only internal cisco users will have stats.CesMonitor module
#  - below code does nothing for DevNet users -  we DO NOT track usage stats
#    for PyPI/public/customer users
from .clean import DeviceClean
