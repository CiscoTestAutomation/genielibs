import re
import unittest
from pyats.topology import loader
from unittest.mock import MagicMock, Mock

from genie.libs.sdk.apis.iosxe.platform.utils import (
    write_erase_reload_device_without_reconfig,\
    write_erase_reload_device
    )


class TestUtilsApi(unittest.TestCase):

    def test_write_erase_reload_device_without_reconfig(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.platform = 'iosxe'
        device.type = 'CSR1000v'
        device.via = 'cli'
        device.execute = Mock()
        device.api.get_username_password = Mock(return_value=['test', 'test'])
        write_erase_reload_device_without_reconfig(device, via_console='cli', reload_timeout=300)

    def test_write_erase_reload_device(self):
        device = MagicMock()
        device.hostname = 'router'
        device.os = 'iosxe'
        device.platform = 'iosxe'
        device.type = 'CSR1000v'
        device.via = 'cli'
        device.execute = Mock()
        device.api.get_username_password = Mock(return_value=['test', 'test'])
        write_erase_reload_device(device, via_console='cli', reload_timeout=300, static_route='0.0.0.0',\
         static_route_netmask='0.0.0.0', static_route_nexthop='127.1.1.1', priv=15, vty_start=0, vty_end=4,\
         mgmt_interface='GigabitEthernet1', mgmt_netmask='255.255.255.150', config_sleep=10,\
         vrf='Mgmt-intf', via_mgmt='vty', post_reconnect_time=10)

