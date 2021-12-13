'''
    Module:
        genie.libs.clean

    Description:
        This is the sub-component of Genie for `genie.libs.clean`.

'''

# metadata
__version__ = '21.12'
__author__ = 'Cisco Systems Inc.'
__contact__ = ['asg-genie-support@cisco.com', 'pyats-support-ext@cisco.com']
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'


from genie import abstract
abstract.declare_package(__name__)

from .clean import DeviceClean, PyatsDeviceClean, BaseStage
