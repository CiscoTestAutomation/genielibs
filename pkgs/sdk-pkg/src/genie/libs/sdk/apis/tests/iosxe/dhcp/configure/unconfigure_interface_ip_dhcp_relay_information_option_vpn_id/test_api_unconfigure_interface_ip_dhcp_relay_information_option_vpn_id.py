from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_dhcp_relay_information_option_vpn_id


class TestUnconfigureInterfaceIpDhcpRelayInformationOptionVpnId(TestCase):

    def test_unconfigure_interface_ip_dhcp_relay_information_option_vpn_id(self):
        self.device = Mock()
        unconfigure_interface_ip_dhcp_relay_information_option_vpn_id(self.device, 'vlan100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface vlan100",
                    "no ip dhcp relay information option vpn-id"],)
          )

