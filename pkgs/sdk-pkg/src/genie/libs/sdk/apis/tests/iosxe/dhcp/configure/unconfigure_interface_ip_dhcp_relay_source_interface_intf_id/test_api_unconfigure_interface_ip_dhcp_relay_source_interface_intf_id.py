from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_dhcp_relay_source_interface_intf_id


class TestUnconfigureInterfaceIpDhcpRelaySourceInterfaceIntfId(TestCase):

    def test_unconfigure_interface_ip_dhcp_relay_source_interface_intf_id(self):
        self.device = Mock()
        unconfigure_interface_ip_dhcp_relay_source_interface_intf_id(self.device, 'vlan100', 'Loopback1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface vlan100",
                    "no ip dhcp relay source-interface Loopback1"],)
          )