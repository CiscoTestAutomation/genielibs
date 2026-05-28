import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_ikev2_profile


class TestUnconfigureIkev2Profile(TestCase):

    def test_unconfigure_ikev2_profile(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ikev2_profile(device, "ikev2_prof10")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("no crypto ikev2 profile ikev2_prof10", sent_commands)


if __name__ == "__main__":
    unittest.main()