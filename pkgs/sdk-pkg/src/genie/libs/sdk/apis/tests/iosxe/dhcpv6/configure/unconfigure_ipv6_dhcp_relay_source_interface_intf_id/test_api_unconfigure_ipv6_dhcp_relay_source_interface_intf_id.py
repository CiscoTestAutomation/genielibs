from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_relay_source_interface_intf_id
from unittest.mock import Mock

class TestUnconfigureIpv6DhcpRelaySourceInterfaceIntfId(TestCase):

    def test_unconfigure_ipv6_dhcp_relay_source_interface_intf_id(self):
        self.device = Mock()
        unconfigure_ipv6_dhcp_relay_source_interface_intf_id(self.device, 'Vlan1500', 'Loopback1')
        self.device.configure.assert_called_with(['interface Vlan1500', 'no ipv6 dhcp relay source-interface Loopback1'])
   
