import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.hardware.configure import configure_hw_module_breakout


class TestConfigureHwModuleBreakout(TestCase):

    def test_configure_hw_module_breakout(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_hw_module_breakout(device, None, None, '1', '1', '1')

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('hw-module breakout module 1 port 1 switch 1', cfg_lines)


if __name__ == '__main__':
    unittest.main()