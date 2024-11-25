import unittest
from genie.libs.sdk.apis.iosxe.aaa.configure import disable_aaa_authentication_login
from unittest.mock import Mock

class TestDisableAaaAuthenticationLogin(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_disable_aaa_authentication_login(self):
        disable_aaa_authentication_login(self.device, 'default', 'local', auth_db2=None)
        self.device.configure.assert_called_once_with(
            'no aaa authentication login default local'
        )
