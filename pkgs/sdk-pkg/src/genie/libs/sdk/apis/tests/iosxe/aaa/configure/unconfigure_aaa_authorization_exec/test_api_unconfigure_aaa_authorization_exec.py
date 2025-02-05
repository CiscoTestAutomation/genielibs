from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_authorization_exec
from unittest.mock import Mock


class TestUnconfigureAaaAuthorizationExec(TestCase):

    def test_unconfigure_aaa_authorization_exec(self):
        self.device = Mock()
        result = unconfigure_aaa_authorization_exec(self.device, 'CON_author')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no aaa authorization exec CON_author',)
        )
