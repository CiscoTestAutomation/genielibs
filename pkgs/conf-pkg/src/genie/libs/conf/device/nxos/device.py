'''
Device class for devices with nxos OS.
'''

__all__ = (
    'Device',
)

from enum import Enum
import logging
import re

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

import genie.libs.conf.device
import genie.libs.conf.device.cisco

logger = logging.getLogger(__name__)


class Device(genie.libs.conf.device.cisco.Device):
    '''Device class for devices with nxos OS'''

    logfile_messages_level = managedattribute(
        name='logfile_messages_level',
        default=5,
        type=(None, managedattribute.test_istype(int)))

    def learn_interface_mac_addresses(self):

        cmd = 'show interface mac-address'
        out = self.execute(cmd)
        interface = None
        for line in out.splitlines():
            m = re.match(r'^(?P<interface>\S+) +(?P<mac>[A-Fa-f0-9.:-]+) +(?P<bi_mac>[A-Fa-f0-9.:-]+)$', line)
            if m:
                # NX-OS:
                # mgmt0                      0024.f71a.0fe0  0024.f71a.0fe0
                interface = self.interfaces[m.group('interface')]
                if interface:
                    mac = m.group('mac')
                    bi_mac = m.group('bi_mac')
                    try:
                        if bi_mac:
                            interface.burnin_mac_address = bi_mac
                        if mac != bi_mac:
                            interface.mac_address = mac
                    except AttributeError:
                        # Ok, attribute may be read-only, such as for SubInterface
                        pass
                continue

    def build_config(self, apply=True, attributes=None):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder()

        configurations.append_block(super().build_config(apply=False, attributes=attributes))

        # TODO -- exception dump?
        # nodename
        if attributes.value('nodename'):
            configurations.append_line(
                attributes.format('hostname {nodename}'))

        if apply:
            if configurations:
                self.configure(str(configurations), fail_invalid=True)
        else:
            # Return configuration
            return CliConfig(device=self, unconfig=False,
                             cli_config=configurations, fail_invalid=True)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder()

        configurations.append_block(
            super().build_unconfig(apply=False, attributes=attributes,
                                   **kwargs))

        if apply:
            if configurations:
                self.configure(str(configurations), fail_invalid=True)
        else:
            # Return configuration
            return CliConfig(device=self, unconfig=True,
                             cli_config=configurations, fail_invalid=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

