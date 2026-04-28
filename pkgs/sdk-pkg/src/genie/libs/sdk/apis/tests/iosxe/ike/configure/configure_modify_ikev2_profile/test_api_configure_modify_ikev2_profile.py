import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_modify_ikev2_profile


class TestConfigureModifyIkev2Profile(TestCase):

    def test_configure_modify_ikev2_profile(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_modify_ikev2_profile(
            device,
            "IKEV2_PROFILE",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            True,
            "Mgmt-intf",
            1,
            "group cert list local-group flex",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 profile IKEV2_PROFILE", sent_commands)
        self.assertIn("nat force-encap", sent_commands)
        self.assertIn("match fvrf Mgmt-intf", sent_commands)
        self.assertIn("virtual-template 1", sent_commands)
        self.assertIn(
            "aaa authorization group cert list local-group flex",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()