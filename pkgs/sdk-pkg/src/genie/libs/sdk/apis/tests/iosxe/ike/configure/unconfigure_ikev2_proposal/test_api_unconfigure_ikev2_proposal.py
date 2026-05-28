import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_ikev2_proposal


class TestUnconfigureIkev2Proposal(TestCase):

    def test_unconfigure_ikev2_proposal(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ikev2_proposal(device, "prof1")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("no crypto ikev2 proposal prof1", sent_commands)


if __name__ == "__main__":
    unittest.main()