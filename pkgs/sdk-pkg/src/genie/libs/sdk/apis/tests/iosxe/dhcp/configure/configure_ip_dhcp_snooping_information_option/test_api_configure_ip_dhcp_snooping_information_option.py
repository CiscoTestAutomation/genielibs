import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_snooping_information_option


class TestConfigureIpDhcpSnoopingInformationOption(TestCase):

    def test_configure_ip_dhcp_snooping_information_option(self):
        device = Mock()
        result = configure_ip_dhcp_snooping_information_option(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip dhcp snooping information option',)
        )


if __name__ == '__main__':
    unittest.main()