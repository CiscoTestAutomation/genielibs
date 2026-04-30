import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import (
    configure_ikev2_authorization_policy,
)


class TestConfigureIkev2AuthorizationPolicy(TestCase):

    def test_configure_ikev2_authorization_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_authorization_policy(
            device,
            "flex", False, None, None, None, None, None, None, None, None, None,
            "197:16:1::", 64,
            None, None, None, None, None, None, None, None, None,
            False, None, None, None, None, None, None, None, None, None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 authorization policy flex", sent_commands)
        self.assertIn("route set remote ipv6 197:16:1::/64", sent_commands)


if __name__ == "__main__":
    unittest.main()