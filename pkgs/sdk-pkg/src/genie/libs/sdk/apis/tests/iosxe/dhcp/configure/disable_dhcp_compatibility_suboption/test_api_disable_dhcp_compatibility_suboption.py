import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import disable_dhcp_compatibility_suboption


class TestDisableDhcpCompatibilitySuboption(TestCase):

    def test_disable_dhcp_compatibility_suboption(self):
        device = Mock()
        result = disable_dhcp_compatibility_suboption(device, 'link-selection')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip dhcp compatibility suboption link-selection',)
        )


if __name__ == '__main__':
    unittest.main()