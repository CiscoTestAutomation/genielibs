import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_class


class TestUnconfigureIpDhcpClass(TestCase):

    def test_unconfigure_ip_dhcp_class(self):
        """Verify no ip dhcp class emits correct CLI command."""
        device = Mock()
        result = unconfigure_ip_dhcp_class(device, class_name='DS_CLASS')
        self.assertIsNone(result)
        device.configure.assert_called_once_with('no ip dhcp class DS_CLASS')

    def test_unconfigure_ip_dhcp_class_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_ip_dhcp_class(device, class_name='DS_CLASS')


if __name__ == '__main__':
    unittest.main()
