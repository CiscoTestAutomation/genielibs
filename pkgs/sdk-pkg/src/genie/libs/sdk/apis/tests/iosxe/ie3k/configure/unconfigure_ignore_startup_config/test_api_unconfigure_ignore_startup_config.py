from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ie3k.configure import unconfigure_ignore_startup_config

class TestUnconfigureIgnoreStartupConfig(TestCase):

    def test_unconfigure_ignore_startup_config(self):
        self.device = Mock()
        self.device.subconnections = []

        self.device.state_machine = Mock()
        self.device.state_machine.current_state = 'enable'
        self.device.configure = Mock()
        self.device.execute = Mock()

        unconfigure_ignore_startup_config(self.device)

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no system ignore startupconfig switch all',)
        )
