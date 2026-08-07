import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import unconfigure_ipsec_df_bit


class TestUnconfigureIpsecDfBit(TestCase):

    def test_unconfigure_ipsec_df_bit(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ipsec_df_bit(
            device,
            False,
            True,
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no crypto ipsec df-bit copy"],
        )


if __name__ == "__main__":
    unittest.main()
