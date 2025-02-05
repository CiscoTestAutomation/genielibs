from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_login_authentication_on_vty
from unittest.mock import Mock


class TestUnconfigureLoginAuthenticationOnVty(TestCase):

    def test_unconfigure_login_authentication_on_vty(self):
        self.device = Mock()
        result = unconfigure_login_authentication_on_vty(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 15', 'no login authentication'],)
        )
