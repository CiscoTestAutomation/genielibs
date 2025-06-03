from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ie3k.configure import configure_ignore_startup_config

class TestConfigureIgnoreStartupConfig(TestCase):

    def test_configure_ignore_startup_config(self):
        self.device = Mock()
        self.device.subconnections = []

        self.device.state_machine = Mock()
        self.device.state_machine.current_state = 'enable'
        self.device.configure = Mock()
        self.device.execute = Mock()

        configure_ignore_startup_config(self.device)

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('system ignore startupconfig switch all',)
        )
