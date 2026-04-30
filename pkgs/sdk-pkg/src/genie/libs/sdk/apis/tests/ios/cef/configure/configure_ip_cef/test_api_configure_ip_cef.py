from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.cef.configure import configure_ip_cef


class TestConfigureIpCef(TestCase):

    def test_configure_ip_cef(self):
        self.device = Mock()
        configure_ip_cef(self.device)
        self.device.configure.assert_called_once_with(
            "ip cef"
        )
