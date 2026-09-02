import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_ip_ssh_server_algorithm_hostkey,
)


class TestConfigureIpSshServerAlgorithmHostkey(TestCase):

    def test_configure_ip_ssh_server_algorithm_hostkey(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_ssh_server_algorithm_hostkey(
            device,
            "rsa-sha2-256",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "ip ssh server algorithm hostkey rsa-sha2-256",
        )


if __name__ == "__main__":
    unittest.main()
