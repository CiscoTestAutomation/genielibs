from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_exec_default_group_if_authenticated
from unittest.mock import Mock


class TestConfigureAaaAuthorizationExecDefaultGroupIfAuthenticated(TestCase):

    def test_configure_aaa_authorization_exec_default_group_if_authenticated(self):
        self.device = Mock()
        configure_aaa_authorization_exec_default_group_if_authenticated(self.device, 'TACACS-group')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authorization exec default group TACACS-group if-authenticated',)
        )

