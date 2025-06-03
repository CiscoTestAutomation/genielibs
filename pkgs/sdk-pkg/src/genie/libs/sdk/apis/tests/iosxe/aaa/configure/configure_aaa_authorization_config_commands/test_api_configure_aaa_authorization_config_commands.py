from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_authorization_config_commands
from unittest.mock import Mock


class TestConfigureAaaAccountingConnectionDefaultStartStopGroupTacacsGroup(TestCase):

    def test_configure_aaa_authorization_config_commands(self):
        self.device = Mock()
        configure_aaa_authorization_config_commands(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('aaa authorization config-commands',)
        )

