from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.debug.configure import disable_debug


class TestDisableDebug(TestCase):

    def test_disable_debug_ipv6_nd(self):
        self.device = Mock()
        disable_debug(self.device, 'ipv6 nd')
        self.device.execute.assert_called_once_with(
            "no debug ipv6 nd"
        )

    def test_disable_debug_dhcp(self):
        self.device = Mock()
        disable_debug(self.device, 'dhcp')
        self.device.execute.assert_called_once_with(
            "no debug dhcp"
        )

    def test_disable_debug_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            disable_debug(self.device, 'ipv6 nd')
