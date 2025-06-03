from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_network_default_group
from unittest.mock import Mock


class TestConfigureAaaAuthorizationNetworkDefaultGroup(TestCase):

    def test_configure_aaa_authorization_exec_default_group_if_authenticated(self):
        self.device = Mock()
        configure_aaa_authorization_network_default_group(self.device, 'TACACS-group')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authorization network default group TACACS-group',)
        )

