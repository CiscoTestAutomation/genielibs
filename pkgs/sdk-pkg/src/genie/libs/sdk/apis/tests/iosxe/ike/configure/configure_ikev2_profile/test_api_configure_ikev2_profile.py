import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_profile


class TestConfigureIkev2Profile(TestCase):

    def test_configure_ikev2_profile(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_profile(
            device,
            "IKEV2_PROFILE_NAME_V4",
            "198.51.100.10 255.255.255.255",
            "pre-share",
            "pre-share",
            "IKEV2-KEYRING-PPK-3",
            10,
            2,
            "on-demand",
            "any",
            "IKEV2-KEYRING-PPK-3",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 profile IKEV2_PROFILE_NAME_V4", sent_commands)
        self.assertIn("match fvrf any", sent_commands)
        self.assertIn(
            "match identity remote address 198.51.100.10 255.255.255.255",
            sent_commands,
        )
        self.assertIn("authentication remote pre-share", sent_commands)
        self.assertIn("authentication local pre-share", sent_commands)
        self.assertIn("keyring local IKEV2-KEYRING-PPK-3", sent_commands)
        self.assertIn("keyring ppk IKEV2-KEYRING-PPK-3", sent_commands)
        self.assertIn("dpd 10 2 on-demand", sent_commands)


if __name__ == "__main__":
    unittest.main()