import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.hardware.configure import configure_400g_mode_for_port_group


class TestConfigure400gModeForPortGroup(TestCase):

    def test_configure_400g_mode_for_port_group(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        result = configure_400g_mode_for_port_group(device, '2', '2')

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions (API may pass list or multiline string)
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('hw-module slot 2 port-group 2 mode 400G', cfg_lines)


if __name__ == '__main__':
    unittest.main()