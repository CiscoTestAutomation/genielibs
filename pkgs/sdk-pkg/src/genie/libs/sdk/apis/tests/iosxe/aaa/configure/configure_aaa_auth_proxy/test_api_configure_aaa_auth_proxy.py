import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_auth_proxy


class TestConfigureAaaAuthProxy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_auth_proxy(self):
        configure_aaa_auth_proxy(self.device, 'ISEGRP')
        self.device.configure.assert_called_once_with([
            'aaa authorization auth-proxy default group ISEGRP'
        ])
