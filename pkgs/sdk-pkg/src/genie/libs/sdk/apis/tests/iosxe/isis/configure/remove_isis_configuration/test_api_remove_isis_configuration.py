import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import remove_isis_configuration


class TestRemoveIsisConfiguration(TestCase):

    def test_remove_isis_configuration(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = remove_isis_configuration(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no router isis"],
        )


if __name__ == "__main__":
    unittest.main()
