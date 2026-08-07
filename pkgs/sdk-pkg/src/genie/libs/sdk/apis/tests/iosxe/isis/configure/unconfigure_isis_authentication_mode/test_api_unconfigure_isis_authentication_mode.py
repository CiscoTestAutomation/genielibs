import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import (
    unconfigure_isis_authentication_mode,
)


class TestUnconfigureIsisAuthenticationMode(TestCase):

    def test_unconfigure_isis_authentication_mode(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_isis_authentication_mode(
            device,
            "Te1/0/10",
            "md5",
            "Level-1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Te1/0/10",
                "no isis authentication mode md5 Level-1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
