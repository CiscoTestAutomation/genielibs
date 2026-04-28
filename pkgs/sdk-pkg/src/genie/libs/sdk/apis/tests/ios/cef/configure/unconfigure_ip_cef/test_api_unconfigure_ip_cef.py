from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.cef.configure import unconfigure_ip_cef


class TestUnconfigureIpCef(TestCase):

    def test_unconfigure_ip_cef(self):
        self.device = Mock()
        unconfigure_ip_cef(self.device)
        self.device.configure.assert_called_once_with(
            "no ip cef"
        )
