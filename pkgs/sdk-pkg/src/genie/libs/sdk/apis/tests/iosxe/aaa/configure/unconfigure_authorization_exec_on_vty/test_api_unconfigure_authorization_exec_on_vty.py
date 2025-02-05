from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_authorization_exec_on_vty
from unittest.mock import Mock


class TestUnconfigureAuthorizationExecOnVty(TestCase):

    def test_unconfigure_authorization_exec_on_vty(self):
        self.device = Mock()
        result = unconfigure_authorization_exec_on_vty(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 15', 'no authorization exec'],)
        )
