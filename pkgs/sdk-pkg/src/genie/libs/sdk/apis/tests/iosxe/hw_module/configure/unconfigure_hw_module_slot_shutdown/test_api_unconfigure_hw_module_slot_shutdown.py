import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.hw_module.configure import (
    unconfigure_hw_module_slot_shutdown,
)


class TestUnconfigureHwModuleSlotShutdown(TestCase):

    def test_unconfigure_hw_module_slot_shutdown(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_hw_module_slot_shutdown(device, "2")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("no hw-module slot 2 shutdown", sent_commands)


if __name__ == "__main__":
    unittest.main()