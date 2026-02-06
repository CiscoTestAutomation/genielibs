from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat8k.configure import configure_breakout_cli


class TestConfigureBreakoutCli(TestCase):

    def test_configure_breakout_cli(self):
        device = Mock()
        result = configure_breakout_cli(device, 'all', '0/2', '10g', 60)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('hw-module subslot 0/2 breakout 10g port all',)
        )
