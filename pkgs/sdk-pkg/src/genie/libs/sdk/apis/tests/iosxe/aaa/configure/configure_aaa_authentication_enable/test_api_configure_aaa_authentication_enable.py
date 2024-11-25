import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authentication_enable


class TestConfigureAaaAuthenticationEnable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_authentication_enable(self):
        configure_aaa_authentication_enable(self.device, 'group', 'DATANET', 'enable')
        self.device.configure.assert_called_once_with(
            'aaa authentication enable default group DATANET enable'
        )
