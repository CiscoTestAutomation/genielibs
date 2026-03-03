import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import enable_dhcp_smart_relay


class TestEnableDhcpSmartRelay(TestCase):

    def test_enable_dhcp_smart_relay(self):
        device = Mock()
        result = enable_dhcp_smart_relay(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('ip dhcp smart-relay')


if __name__ == '__main__':
    unittest.main()