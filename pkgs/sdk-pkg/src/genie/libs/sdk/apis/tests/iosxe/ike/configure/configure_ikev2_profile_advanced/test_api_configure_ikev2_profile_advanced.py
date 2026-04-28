import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import (
    configure_ikev2_profile_advanced,
)


class TestConfigureIkev2ProfileAdvanced(TestCase):

    def test_configure_ikev2_profile_advanced(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_profile_advanced(
            device,
            "IKEv2_PROFILE",
            None, None, None, None, None, None, None, None, None,
            False, None, False, None, None, None, None, None,
            False, False, None, False, False, False, False,
            None, False, None, None, None, False,
            None, None, None, None, None,
            False, None, False, None, None, None, None, None,
            False, None, "client",
            False, False, None, None, None,
            False, False, None, False, False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 profile IKEv2_PROFILE", sent_commands)


if __name__ == "__main__":
    unittest.main()