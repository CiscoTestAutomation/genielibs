import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import unconfigure_ipsec_sa_global


class TestUnconfigureIpsecSaGlobal(TestCase):

    def test_unconfigure_ipsec_sa_global(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ipsec_sa_global(
            device,
            True,
            True,
            True,
            False,
            False,
            False,
            True,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "no crypto ipsec security-association ecn",
                "no crypto ipsec security-association idle-time",
                "no crypto ipsec security-association lifetime days",
                "no crypto ipsec security-association replay window-size",
                "no crypto ipsec security-association multi-sn",
            ],
        )


if __name__ == "__main__":
    unittest.main()
