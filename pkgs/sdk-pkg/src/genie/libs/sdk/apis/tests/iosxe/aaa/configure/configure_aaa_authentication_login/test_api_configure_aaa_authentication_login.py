import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authentication_login


class TestConfigureAaaAuthenticationLogin(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_authentication_login(self):
        configure_aaa_authentication_login(self.device, 'default', 'local', 'radius')
        self.device.configure.assert_called_once_with(
            'aaa authentication login default local group radius'
        )
