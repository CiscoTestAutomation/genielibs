import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_snooping_track_server_dhcp_acks


class TestConfigureDhcpSnoopingTrackServerDhcpAcks(TestCase):

    def test_configure_dhcp_snooping_track_server_dhcp_acks(self):
        device = Mock()
        result = configure_dhcp_snooping_track_server_dhcp_acks(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip dhcp snooping track server all-dhcp-acks',)
        )


if __name__ == '__main__':
    unittest.main()