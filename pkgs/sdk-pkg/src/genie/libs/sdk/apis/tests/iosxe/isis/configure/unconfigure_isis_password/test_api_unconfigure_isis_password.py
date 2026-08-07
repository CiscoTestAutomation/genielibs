import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import unconfigure_isis_password


class TestUnconfigureIsisPassword(TestCase):

    def test_unconfigure_isis_password(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_isis_password(
            device,
            "Te1/0/10",
            "testpwd",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Te1/0/10",
                "no isis password testpwd",
            ],
        )


if __name__ == "__main__":
    unittest.main()
