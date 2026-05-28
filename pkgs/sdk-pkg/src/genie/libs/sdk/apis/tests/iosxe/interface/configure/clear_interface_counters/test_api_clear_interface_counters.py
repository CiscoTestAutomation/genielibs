import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import clear_interface_counters


class TestClearInterfaceCounters(TestCase):

    def test_clear_interface_counters(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = clear_interface_counters(device, "Fo1/1/1", 90)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual("clear counters Fo1/1/1", sent_command)


if __name__ == "__main__":
    unittest.main()