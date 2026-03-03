import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import disable_dhcp_snooping_glean


class TestDisableDhcpSnoopingGlean(TestCase):

    def test_disable_dhcp_snooping_glean(self):
        device = Mock()
        result = disable_dhcp_snooping_glean(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('no ip dhcp snooping glean')


if __name__ == '__main__':
    unittest.main()