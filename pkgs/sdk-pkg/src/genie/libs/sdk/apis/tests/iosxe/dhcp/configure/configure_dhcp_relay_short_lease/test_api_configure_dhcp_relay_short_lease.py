import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_relay_short_lease


class TestConfigureDhcpRelayShortLease(TestCase):

    def test_configure_dhcp_relay_short_lease(self):
        device = Mock()
        result = configure_dhcp_relay_short_lease(device, 60, False)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp-relay short-lease 60'],)
        )


if __name__ == '__main__':
    unittest.main()