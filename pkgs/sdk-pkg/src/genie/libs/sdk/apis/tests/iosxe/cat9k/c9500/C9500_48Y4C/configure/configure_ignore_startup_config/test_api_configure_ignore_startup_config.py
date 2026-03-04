from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9500.C9500_48Y4C.configure import configure_ignore_startup_config

class TestConfigureIgnoreStartupConfig(TestCase):

    def test_configure_ignore_startup_config(self):
        device = Mock()
        device.subconnections = None
        device.state_machine.current_state = 'enable'
        device.role = 'active'
        result = configure_ignore_startup_config(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('system ignore startupconfig',)
        )