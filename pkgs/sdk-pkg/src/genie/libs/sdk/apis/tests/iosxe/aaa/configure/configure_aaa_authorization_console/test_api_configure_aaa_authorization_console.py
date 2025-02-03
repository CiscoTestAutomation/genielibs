from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_console
from unittest.mock import Mock


class TestConfigureAaaAuthorizationConsole(TestCase):

    def test_configure_aaa_authorization_console(self):
        self.device = Mock()
        result = configure_aaa_authorization_console(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authorization console',)
        )
