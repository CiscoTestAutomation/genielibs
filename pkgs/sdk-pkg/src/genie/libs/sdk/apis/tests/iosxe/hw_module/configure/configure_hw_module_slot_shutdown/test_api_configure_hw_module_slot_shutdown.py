import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.hw_module.configure import configure_hw_module_slot_shutdown


class TestConfigureHwModuleSlotShutdown(TestCase):

    def test_configure_hw_module_slot_shutdown(self):
        device = Mock()
        device.state_machine.current_state = 'enable'

        output = (
            'hw-module slot 2 shutdown\r\n'
            '%Shutdown Command is being executed for slot 2\r\n\r\n'
            '%Please wait for a minute, before doing any further operations on this card\r\n\r\n'
        )
        device.configure.return_value = output

        result = configure_hw_module_slot_shutdown(device, '2')

        expected_output = output
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()

        # Validate commands passed to device.configure(...)
        cfg_arg = device.configure.mock_calls[0].args[0]

        # Normalize to list for assertions
        if isinstance(cfg_arg, str):
            cfg_lines = [line.strip() for line in cfg_arg.splitlines() if line.strip()]
        else:
            cfg_lines = list(cfg_arg)

        self.assertIn('hw-module slot 2 shutdown', cfg_lines)


if __name__ == '__main__':
    unittest.main()