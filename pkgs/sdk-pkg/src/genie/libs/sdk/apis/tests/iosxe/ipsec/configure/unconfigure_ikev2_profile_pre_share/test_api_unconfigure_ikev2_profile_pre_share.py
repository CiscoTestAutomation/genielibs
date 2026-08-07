import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    unconfigure_ikev2_profile_pre_share,
)


class TestUnconfigureIkev2ProfilePreShare(TestCase):

    def test_unconfigure_ikev2_profile_pre_share(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ikev2_profile_pre_share(
            device,
            "test_ike_profile",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no crypto ikev2 profile test_ike_profile"],
        )


if __name__ == "__main__":
    unittest.main()
