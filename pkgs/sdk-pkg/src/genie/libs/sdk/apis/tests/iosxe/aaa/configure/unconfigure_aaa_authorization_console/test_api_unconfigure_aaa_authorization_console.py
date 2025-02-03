from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_authorization_console
from unittest.mock import Mock


class TestUnconfigureAaaAuthorizationConsole(TestCase):

    def test_unconfigure_aaa_authorization_console(self):
        self.device = Mock()
        result = unconfigure_aaa_authorization_console(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no aaa authorization console',)
        )
