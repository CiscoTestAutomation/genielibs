import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_snooping_database


class TestConfigureIpDhcpSnoopingDatabase(TestCase):

    def test_configure_ip_dhcp_snooping_database(self):
        device = Mock()
        result = configure_ip_dhcp_snooping_database(device, 'bootflash:dhcpsnoop.db', False, '10')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
              # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip dhcp snooping database bootflash:dhcpsnoop.db'],)
        )

if __name__ == '__main__':
    unittest.main()