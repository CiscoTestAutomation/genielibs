import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    unconfigure_ip_ssh_version,
)


class TestUnconfigureIpSshVersion(TestCase):

    def test_unconfigure_ip_ssh_version(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_ssh_version(
            device,
            2,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no ip ssh version 2",
        )


if __name__ == "__main__":
    unittest.main()
