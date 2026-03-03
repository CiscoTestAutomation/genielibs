import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import disable_ip_dhcp_auto_broadcast


class TestDisableIpDhcpAutoBroadcast(TestCase):

    def test_disable_ip_dhcp_auto_broadcast(self):
        device = Mock()
        result = disable_ip_dhcp_auto_broadcast(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('no ip dhcp auto-broadcast')


if __name__ == '__main__':
    unittest.main()