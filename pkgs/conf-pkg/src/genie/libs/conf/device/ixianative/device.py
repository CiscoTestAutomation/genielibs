'''
Device class for Ixia traffic generator device

Requirements:
    * IxOS/IxVM 7.40 or higher
    * IxNetork EA version 7.40 or higher
'''

# Genie Devices
from genie.libs.conf.device.cisco import Device as CiscoDevice


class Device(CiscoDevice):
    '''Device class for Ixia traffic generator device
    __init__ instantiates a single connection instance.'''

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
