import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import enable_dhcp_relay_information_option


class TestEnableDhcpRelayInformationOption(TestCase):

    def test_enable_dhcp_relay_information_option(self):
        device = Mock()
        result = enable_dhcp_relay_information_option(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('ip dhcp relay information option')

    def test_enable_dhcp_relay_information_option_with_vpn(self):
        device = Mock()
        result = enable_dhcp_relay_information_option(device, vpn=True)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('ip dhcp relay information option vpn')


if __name__ == '__main__':
    unittest.main()