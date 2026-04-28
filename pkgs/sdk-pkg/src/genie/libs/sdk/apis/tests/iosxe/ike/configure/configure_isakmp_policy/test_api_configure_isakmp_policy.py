import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_isakmp_policy


class TestConfigureIsakmpPolicy(TestCase):

    def test_configure_isakmp_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isakmp_policy(
            device,
            "666",
            "pre-share",
            "aes 256",
            "24",
            "sha512",
            None,
            "56789",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto isakmp policy 666", sent_commands)
        self.assertIn("authentication pre-share", sent_commands)
        self.assertIn("encryption aes 256", sent_commands)
        self.assertIn("group 24", sent_commands)
        self.assertIn("hash sha512", sent_commands)
        self.assertIn("lifetime 56789", sent_commands)

    def test_configure_isakmp_policy_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isakmp_policy(
            device,
            "123",
            None,
            None,
            None,
            None,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto isakmp policy 123", sent_commands)


if __name__ == "__main__":
    unittest.main()