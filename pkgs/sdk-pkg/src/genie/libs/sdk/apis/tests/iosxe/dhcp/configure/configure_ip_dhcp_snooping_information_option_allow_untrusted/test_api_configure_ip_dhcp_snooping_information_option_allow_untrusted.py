import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_snooping_information_option_allow_untrusted


class TestConfigureIpDhcpSnoopingInformationOptionAllowUntrusted(TestCase):

    def test_configure_ip_dhcp_snooping_information_option_allow_untrusted(self):
        device = Mock()
        result = configure_ip_dhcp_snooping_information_option_allow_untrusted(device, 'Port-channel 93')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Port-channel 93', 'ip dhcp snooping information option allow-untrusted'],)
        )


if __name__ == '__main__':
    unittest.main()