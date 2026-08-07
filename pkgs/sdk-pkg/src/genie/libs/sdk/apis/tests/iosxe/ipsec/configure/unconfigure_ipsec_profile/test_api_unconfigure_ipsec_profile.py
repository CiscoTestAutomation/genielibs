import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import unconfigure_ipsec_profile


class TestUnconfigureIpsecProfile(TestCase):

    def test_unconfigure_ipsec_profile(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ipsec_profile(device, "test_ipsecProfile")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no crypto ipsec profile test_ipsecProfile"],
        )


if __name__ == "__main__":
    unittest.main()
