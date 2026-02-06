import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_client


class TestConfigureIpDhcpClient(TestCase):

    def test_configure_ip_dhcp_client(self):
        device = Mock()
        result = configure_ip_dhcp_client(device, 'broadcast-flag')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip dhcp-client broadcast-flag',)
        )


if __name__ == '__main__':
    unittest.main()