import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_authorization_commands


class TestUnconfigureAaaAuthorizationCommands(unittest.TestCase):

    def test_unconfigure_aaa_authorization_commands(self):
        self.device = Mock()
        unconfigure_aaa_authorization_commands(self.device, '15', 'test', 'local', None)
        self.device.configure.assert_called_with(
            'no aaa authorization commands 15 test local'
        )
