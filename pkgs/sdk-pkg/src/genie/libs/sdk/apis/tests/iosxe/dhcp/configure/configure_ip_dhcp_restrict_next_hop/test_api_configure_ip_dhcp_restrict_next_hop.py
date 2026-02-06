import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_restrict_next_hop


class TestConfigureIpDhcpRestrictNextHop(TestCase):

    def test_configure_ip_dhcp_restrict_next_hop(self):
        device = Mock()
        result = configure_ip_dhcp_restrict_next_hop(device, 'GigabitEthernet1/0/1', 'both')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'ip dhcp restrict-next-hop both'],)
        )


if __name__ == '__main__':
    unittest.main()