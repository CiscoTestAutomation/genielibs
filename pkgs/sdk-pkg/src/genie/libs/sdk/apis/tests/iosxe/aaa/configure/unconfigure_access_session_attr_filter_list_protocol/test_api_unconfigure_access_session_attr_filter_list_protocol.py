import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_access_session_attr_filter_list_protocol


class TestUnconfigureAccessSessionAttrFilterListProtocol(unittest.TestCase):

    def test_unconfigure_access_session_attr_filter_list_protocol(self):
        self.device = Mock()
        unconfigure_access_session_attr_filter_list_protocol(
            self.device,
            'aaa_attr',
            'vlan-id',
            'cdp',
            'dhcp',
            'lldp',
            'dhcpv6',
            'http')
        self.device.configure.assert_called_with([
            'access-session attributes filter-list list aaa_attr',
            'no vlan-id',
            'no cdp',
            'no dhcp',
            'no lldp',
            'no dhcpv6',
            'no http'
        ])
