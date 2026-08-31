import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    unconfigure_ssh_server_algorithm,
)


class TestUnconfigureSshServerAlgorithm(TestCase):

    def test_unconfigure_ssh_server_algorithm(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ssh_server_algorithm(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "default ip ssh server algorithm mac",
                "default ip ssh server algorithm kex",
            ],
        )


if __name__ == "__main__":
    unittest.main()
