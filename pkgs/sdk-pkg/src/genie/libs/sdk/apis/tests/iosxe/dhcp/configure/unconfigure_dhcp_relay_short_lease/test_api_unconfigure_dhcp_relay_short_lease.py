import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_relay_short_lease


class TestUnconfigureDhcpRelayShortLease(TestCase):

    def test_unconfigure_dhcp_relay_short_lease(self):
        device = Mock()
        result = unconfigure_dhcp_relay_short_lease(device, 60, False)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with(['no ip dhcp-relay short-lease 60'])

    def test_unconfigure_dhcp_relay_short_lease_with_interface(self):
        device = Mock()
        result = unconfigure_dhcp_relay_short_lease(device, 60, 'GigabitEthernet1/0/1')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with([
            'interface GigabitEthernet1/0/1',
            'no ip dhcp relay short-lease 60'
        ])


if __name__ == '__main__':
    unittest.main()