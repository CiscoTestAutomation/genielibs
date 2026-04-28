from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.debug.configure import enable_debug


class TestEnableDebug(TestCase):

    def test_enable_debug_ipv6_nd(self):
        self.device = Mock()
        enable_debug(self.device, 'ipv6 nd')
        self.device.execute.assert_called_once_with(
            "debug ipv6 nd"
        )

    def test_enable_debug_dhcp(self):
        self.device = Mock()
        enable_debug(self.device, 'dhcp')
        self.device.execute.assert_called_once_with(
            "debug dhcp"
        )

    def test_enable_debug_radius(self):
        self.device = Mock()
        enable_debug(self.device, 'radius')
        self.device.execute.assert_called_once_with(
            "debug radius"
        )

    def test_enable_debug_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            enable_debug(self.device, 'ipv6 nd')
