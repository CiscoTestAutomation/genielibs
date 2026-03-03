import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import disable_dhcp_relay_information_option


class TestDisableDhcpRelayInformationOption(TestCase):

    def test_disable_dhcp_relay_information_option_with_vpn(self):
        device = Mock()
        result = disable_dhcp_relay_information_option(device, 'vpn')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('no ip dhcp relay information option vpn')

    def test_disable_dhcp_relay_information_option_without_vpn(self):
        device = Mock()
        result = disable_dhcp_relay_information_option(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('no ip dhcp relay information option')


if __name__ == '__main__':
    unittest.main()