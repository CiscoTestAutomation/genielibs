import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_access_session_attr_filter_list


class TestConfigureAccessSessionAttrFilterList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_access_session_attr_filter_list(self):
        configure_access_session_attr_filter_list(
            self.device, 'aaa_attr', 'vlan-id', 'cdp', 'dhcp', 'lldp', 'dhcpv6', 'http')
        self.device.configure.assert_called_once_with([
            'access-session attributes filter-list list aaa_attr',
            'vlan-id',
            'cdp',
            'dhcp',
            'lldp',
            'dhcpv6',
            'http'
        ])