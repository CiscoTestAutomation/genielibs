import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    unconfigure_ssh_certificate_profile,
)


class TestUnconfigureSshCertificateProfile(TestCase):

    def test_unconfigure_ssh_certificate_profile(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ssh_certificate_profile(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no ip ssh server certificate profile",
        )


if __name__ == "__main__":
    unittest.main()
