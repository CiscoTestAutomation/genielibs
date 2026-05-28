import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_class


class TestConfigureIpDhcpClass(TestCase):

    def test_configure_ip_dhcp_class(self):
        """Verify ip dhcp class emits correct CLI command."""
        device = Mock()
        result = configure_ip_dhcp_class(device, class_name='DS_CLASS')
        self.assertIsNone(result)
        device.configure.assert_called_once_with('ip dhcp class DS_CLASS')

    def test_configure_ip_dhcp_class_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_ip_dhcp_class(device, class_name='DS_CLASS')


if __name__ == '__main__':
    unittest.main()
