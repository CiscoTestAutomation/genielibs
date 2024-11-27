import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_commands


class TestConfigureAaaAuthorizationCommands(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_aaa_authorization_commands(self):
        configure_aaa_authorization_commands(self.device, '15', 'test', 'local', None)
        self.device.configure.assert_called_once_with(
            'aaa authorization commands 15 test local'
        )
