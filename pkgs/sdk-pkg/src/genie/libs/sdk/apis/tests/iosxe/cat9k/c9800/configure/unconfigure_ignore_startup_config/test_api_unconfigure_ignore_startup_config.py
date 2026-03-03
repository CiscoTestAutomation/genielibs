from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9800.configure import unconfigure_ignore_startup_config

class TestUnconfigureIgnoreStartupConfig(TestCase):

    def test_unconfigure_ignore_startup_config(self):
        device = Mock()
        device.subconnections = None
        device.state_machine.current_state = 'enable'
        device.role = 'active'

        result = unconfigure_ignore_startup_config(device)
        self.assertEqual(result, None)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('config-register 0x2102',)
        )