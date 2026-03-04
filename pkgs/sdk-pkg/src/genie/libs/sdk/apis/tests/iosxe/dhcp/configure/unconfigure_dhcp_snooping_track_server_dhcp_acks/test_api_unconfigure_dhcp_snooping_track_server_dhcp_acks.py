import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_snooping_track_server_dhcp_acks


class TestUnconfigureDhcpSnoopingTrackServerDhcpAcks(TestCase):

    def test_unconfigure_dhcp_snooping_track_server_dhcp_acks(self):
        device = Mock()
        result = unconfigure_dhcp_snooping_track_server_dhcp_acks(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('no ip dhcp snooping track server all-dhcp-acks')


if __name__ == '__main__':
    unittest.main()