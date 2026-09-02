import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_ssh_server_algorithm,
)


class TestConfigureSshServerAlgorithm(TestCase):

    def test_configure_ssh_server_algorithm(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ssh_server_algorithm(
            device,
            "hmac-sha2-512",
            "diffie-hellman-group14-sha1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "ip ssh server algorithm mac hmac-sha2-512",
                "ip ssh server algorithm kex diffie-hellman-group14-sha1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
