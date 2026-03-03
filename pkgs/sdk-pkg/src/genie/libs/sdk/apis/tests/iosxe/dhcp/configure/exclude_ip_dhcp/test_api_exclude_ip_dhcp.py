import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import exclude_ip_dhcp


class TestExcludeIpDhcp(TestCase):

    def test_exclude_ip_dhcp(self):
        device = Mock()
        result = exclude_ip_dhcp(device, '6.6.6.0', None)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with(['ip dhcp excluded-address 6.6.6.0'])

    def test_exclude_ip_dhcp_1(self):
        device = Mock()
        result = exclude_ip_dhcp(device, '4.4.4.4', '5.5.5.5')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with(['ip dhcp excluded-address 4.4.4.4 5.5.5.5'])


if __name__ == '__main__':
    unittest.main()