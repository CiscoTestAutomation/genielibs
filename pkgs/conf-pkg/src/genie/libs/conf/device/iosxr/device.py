'''
Device class for devices with iosxr OS.
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
    '''Device class for devices with iosxr OS'''

    def learn_interface_mac_addresses(self):

        cmd = 'show interfaces | include "line protocol\\|Hardware is"'
        cmd = re.escape(cmd)  # XXXJST TODO Csccon bug!
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

        # TODO
        # "logging console disable"
        # "logging monitor disable"
        # "logging buffered [expr 10 * 1024 * 1024]"

        configurations.append_block(
            super().build_config(apply=False, attributes=attributes))

        # TODO
        # switch -regexp -- [enaTbGetTestDeviceParam $router -platform] {
        #     {^ncs4\d\d\d$} -
        #     {^ncs5\d\d\d$} -
        #     {^ncs6\d\d\d$} -
        #     {^ng$} -
        #     {^crs-ng$} -
        #     {^enxr$} {
        #         #exception choice not supported on these
        #         continue
        #     }
        #
        #     default {
        #         enaGetTftpServerInfo arr_tftp_info -router $router -default_sub_dir "hfr-mpls" ;# XXXJST /hfr-mpls ???
        #         if { [info exists arr_tftp_info(tftp_addr)] } {
        #             lappend cfgs($router) \
        #                 "exception choice [incr choice] compress on filepath\
        #                     tftp://$arr_tftp_info(tftp_addr)/$arr_tftp_info(sub_dir)"
        #         }
        #         if { $img_type eq "ena" } {
        #             lappend cfgs($router) \
        #                 "exception choice [incr choice] compress on filepath disk0:"
        #         } else {
        #             switch -regexp -- [enaTbGetTestDeviceParam $router -platform] {
        #                 {^xrvr$} {
        #                     lappend cfgs($router) \
        #                         "exception choice [incr choice] compress on filepath disk0:"
        #                 }
        #                 {^xrv9\d\d\d$} {
        #                     lappend cfgs($router) \
        #                         "exception choice [incr choice] filepath harddisk:"
        #                 }
        #                 default {
        #                     lappend cfgs($router) \
        #                         "exception choice [incr choice] compress on filepath harddisk:"
        #                 }
        #             }
        #         }
        #     }
        # }

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

    def get_connected_node(self, connection=None):
        try:
            return self.connected_node
        except AttributeError:
            pass
        if not connection:
            connectionmgr = self.connectionmgr
            connection = connectionmgr.connections[connectionmgr.default_alias]
        output = connection.execute('')

        # '\rRP/0/0/CPU0:'
        m = re.match(r'^RP/(?P<node>\d+(?:/(?:RP|RSP|CPU)?\d+)+):',
                     output.strip())
        if not m:
            raise ValueError(
                'Cannot determine {} connected node from prompt {}'.format(
                    self.name,
                    re.escape(output)))
        node = m.group('node')

        return node

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

