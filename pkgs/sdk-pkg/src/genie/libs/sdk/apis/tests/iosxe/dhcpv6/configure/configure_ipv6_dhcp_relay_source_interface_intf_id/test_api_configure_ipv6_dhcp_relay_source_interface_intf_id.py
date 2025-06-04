from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_source_interface_intf_id
from unittest.mock import Mock

class TestConfigureIpv6DhcpRelaySourceInterfaceIntfId(TestCase):

    def test_configure_ipv6_dhcp_relay_source_interface_intf_id(self):
        self.device = Mock()
        configure_ipv6_dhcp_relay_source_interface_intf_id(self.device, 'Vlan1500', 'Loopback1')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['interface Vlan1500', 'ipv6 dhcp relay source-interface Loopback1'],))