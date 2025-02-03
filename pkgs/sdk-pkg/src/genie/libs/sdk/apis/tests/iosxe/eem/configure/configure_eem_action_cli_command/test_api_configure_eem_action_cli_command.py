from unittest import TestCase
from genie.libs.sdk.apis.iosxe.eem.configure import configure_eem_action_cli_command
from unittest.mock import Mock


class TestConfigureEemActionCliCommand(TestCase):

    def test_configure_eem_action_cli_command(self):
        self.device = Mock()
        result = configure_eem_action_cli_command(self.device, 'WRITE_MEM_EEM', 1.0, 'enable')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['event manager applet WRITE_MEM_EEM', 'action 1.0 cli command "enable"'],)
        )
