import unittest
from genie.libs.sdk.apis.iosxe.aaa.configure import enable_aaa_authentication_login
from unittest.mock import Mock

class TestEnableAaaAuthenticationLogin(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_enable_aaa_authentication_login(self):
        enable_aaa_authentication_login(self.device, 'default', 'local', 'tacacs+')
        self.device.configure.assert_called_once_with(
            'aaa authentication login default local tacacs+'
        )
