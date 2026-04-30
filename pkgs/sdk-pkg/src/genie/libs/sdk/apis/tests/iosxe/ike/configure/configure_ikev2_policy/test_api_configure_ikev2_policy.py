import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_policy


class TestConfigureIkev2Policy(TestCase):

    def test_configure_ikev2_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_policy(
            device,
            "IKEv2_POLICY",
            "IKEv2_PROPOSAL",
            "1.1.1.1",
            10,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 policy IKEv2_POLICY", sent_commands)
        self.assertIn("proposal IKEv2_PROPOSAL", sent_commands)
        self.assertIn("match address local 1.1.1.1", sent_commands)
        self.assertIn("match fvrf 10", sent_commands)


if __name__ == "__main__":
    unittest.main()