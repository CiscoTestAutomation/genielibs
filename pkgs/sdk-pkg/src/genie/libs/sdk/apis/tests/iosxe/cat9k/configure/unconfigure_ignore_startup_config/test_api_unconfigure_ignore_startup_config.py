from unittest import TestCase
from unittest.mock import Mock, call
from genie.libs.sdk.apis.iosxe.cat9k.configure import unconfigure_ignore_startup_config
from unicon.core.errors import SubCommandFailure

class TestUnconfigureIgnoreStartupConfig(TestCase):

    def test_unconfigure_ignore_startup_config(self):
        device = Mock()
        device.subconnections = None
        device.state_machine.current_state = 'enable'
        device.role = 'active'

        result = unconfigure_ignore_startup_config(device)
        self.assertEqual(result, None)

    def test_unconfigure_ignore_startup_config_success_second_command(self):
        """
        Verify fallback behavior: first unconfig command fails, second succeeds.
        """
        device = Mock()
        device.subconnections = None
        device.state_machine.current_state = 'enable'
        device.role = 'active'

        device.configure.side_effect = [
            SubCommandFailure("Simulated failure for 'no system ignore startupconfig switch all'"),
            None
        ]

        unconfigure_ignore_startup_config(device)

        self.assertEqual(device.configure.call_count, 2)
        device.configure.assert_has_calls([
            call('no system ignore startupconfig switch all'),
            call('no system ignore startupconfig'),
        ])
        device.execute.assert_not_called()