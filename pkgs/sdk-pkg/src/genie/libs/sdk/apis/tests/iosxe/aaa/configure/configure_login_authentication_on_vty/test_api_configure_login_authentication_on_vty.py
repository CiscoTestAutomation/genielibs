from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_login_authentication_on_vty
from unittest.mock import Mock


class TestConfigureLoginAuthenticationOnVty(TestCase):

    def test_configure_login_authentication_on_vty(self):
        self.device = Mock()
        result = configure_login_authentication_on_vty(self.device, 'VTY_authen')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['line vty 0 15', 'login authentication VTY_authen'],)
        )
