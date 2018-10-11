'''
Device class for HLTAPI devices with agilent OS.
'''

__all__ = (
    'Device',
)

from enum import Enum
import logging
logger = logging.getLogger(__name__)

from genie.decorator import managedattribute

from genie.libs.conf.device.hltapi import Device as HltapiDevice
import genie.libs.conf.interface.hltapi
from genie.libs.conf.stream import Stream


class Device(HltapiDevice):
    '''Device class for HLTAPI devices with agilent OS'''

    class Hltapi(HltapiDevice.Hltapi):
        '''Hltapi class customized for Agilent.'''

        def traffic_control(self, **kwargs):

            # Optional arg, but fails to stop with port_handle (at least it
            # does for HLTAPI 2.25 2.27 and 2.28)
            kwargs.pop('port_handle', None)

            hltkl = self.pyats_connection.traffic_control(**kwargs)

            return hltkl

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

