from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authentication_login_default_group_local
from unittest.mock import Mock


class TestConfigureAaaAuthenticationLoginDefaultGroupLocal(TestCase):

    def test_configure_aaa_authentication_login_default_group_local(self):
        self.device = Mock()
        configure_aaa_authentication_login_default_group_local(self.device, 'TACACS-group')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authentication login default group TACACS-group local',)
        )

