import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import clear_isis


class TestClearIsis(TestCase):

    def test_clear_isis(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = clear_isis(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(sent_command, "clear isis *")


if __name__ == "__main__":
    unittest.main()
