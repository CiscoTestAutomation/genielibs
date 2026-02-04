from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat8k.configure import unconfigure_breakout_cli


class TestUnconfigureBreakoutCli(TestCase):
    
    def test_unconfigure_breakout_cli(self):
        device = Mock()
        result = unconfigure_breakout_cli(device, 'native_port_8', '10g', '0/2', 60)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no hw-module subslot 0/2 breakout 10g port native_port_8',)
        )
