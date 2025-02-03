from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_exec
from unittest.mock import Mock


class TestConfigureAaaAuthorizationExec(TestCase):

    def test_configure_aaa_authorization_exec(self):
        self.device = Mock()
        result = configure_aaa_authorization_exec(self.device, 'VTY_author', 'local', 'ISE')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authorization exec VTY_author local group ISE',)
        )
