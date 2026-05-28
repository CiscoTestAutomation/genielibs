import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_control_policies


class TestConfigureControlPolicies(TestCase):

    def test_configure_control_policies(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_control_policies(
            device,
            "PMAP_DefaultWiredDot1xClosedAuth_1X_MAB",
            "aaa-available",
            "match-all",
            10,
            None,
            "do-until-failure",
            10,
            "resume",
            "reauthentication",
            None,
            None,
            10,
            None,
            3,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "policy-map type control subscriber "
            "PMAP_DefaultWiredDot1xClosedAuth_1X_MAB",
            sent_commands,
        )
        self.assertIn("event aaa-available match-all", sent_commands)
        self.assertIn("10 class always do-until-failure", sent_commands)
        self.assertIn("10 resume reauthentication", sent_commands)


if __name__ == "__main__":
    unittest.main()