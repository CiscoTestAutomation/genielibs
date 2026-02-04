import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_dhcp_relay_information_option_vpn_id


class TestConfigureInterfaceIpDhcpRelayInformationOptionVpnId(TestCase):

    def test_configure_interface_ip_dhcp_relay_information_option_vpn_id(self):
        device = Mock()
        result = configure_interface_ip_dhcp_relay_information_option_vpn_id(device, 'vlan100')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface vlan100', 'ip dhcp relay information option vpn-id'],)
        )


if __name__ == '__main__':
    unittest.main()