'''
Device class for devices with iosxe OS.
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
    '''Device class for devices with iosxe OS'''

    def learn_interface_mac_addresses(self):

        cmd = 'show interfaces | include line protocol|Hardware is'
        out = self.execute(cmd)
        interface = None
        for line in out.splitlines():
            line = line.rstrip()
            m = re.match(r'^(?i)(?P<interface>\S+) is .* line protocol is', line)
            if m:
                interface = self.interfaces[m.group('interface')]
                # GigabitEthernet0/0/0/0 is administratively down, line protocol is administratively down
                continue
            if interface:
                m = re.match(r'(?i)^ +Hardware is +[^,]+, +address is +(?P<mac>[A-Fa-f0-9.:-]+)(?: \(bia (?P<bi_mac>[A-Fa-f0-9.:-]+)\))?', line) \
                    or re.match(r'(?i)^ +address: +([A-Fa-f0-9.:-]+)(?: \(bia (?P<bi_mac>[A-Fa-f0-9.:-]+)\))?', line)
                if m:
                    # IOS, IOS-XR:
                    #   Hardware is GigabitEthernet, address is 6c9c.ed74.06e8 (bia 6c9c.ed74.06e8)
                    #   Hardware is C6k 1000Mb 802.3, address is 0012.8020.de00 (bia 0012.8020.de00)
                    #   Hardware is Bridge-Group Virtual Interface, address is 02a0.0964.e808
                    # NX-OS:
                    #   address: 547f.eefd.a96a (bia 547f.eefd.a96a)
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

        # TODO - logging levels

        # TODO - IOS: no parser cache

        configurations.append_block(super().build_config(apply=False, attributes=attributes))

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

