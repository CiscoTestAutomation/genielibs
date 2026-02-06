import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_snooping_limit


class TestConfigureIpDhcpSnoopingLimit(TestCase):

    def test_configure_ip_dhcp_snooping_limit(self):
        device = Mock()
        result = configure_ip_dhcp_snooping_limit(device, 'te1/0/1', 10)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/1', 'ip dhcp snooping limit rate 10'],)
        )


if __name__ == '__main__':
    unittest.main()