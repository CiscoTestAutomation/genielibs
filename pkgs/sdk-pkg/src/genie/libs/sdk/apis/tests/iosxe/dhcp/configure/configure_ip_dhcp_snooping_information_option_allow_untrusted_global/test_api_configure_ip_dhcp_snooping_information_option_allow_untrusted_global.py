import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_snooping_information_option_allow_untrusted_global


class TestConfigureIpDhcpSnoopingInformationOptionAllowUntrustedGlobal(TestCase):

    def test_configure_ip_dhcp_snooping_information_option_allow_untrusted_global(self):
        device = Mock()
        result = configure_ip_dhcp_snooping_information_option_allow_untrusted_global(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip dhcp snooping information option allow-untrusted',)
        )


if __name__ == '__main__':
    unittest.main()