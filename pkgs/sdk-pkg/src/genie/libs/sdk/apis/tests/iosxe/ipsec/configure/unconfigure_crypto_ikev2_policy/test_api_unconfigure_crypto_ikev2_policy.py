import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    unconfigure_crypto_ikev2_policy,
)


class TestUnconfigureCryptoIkev2Policy(TestCase):

    def test_unconfigure_crypto_ikev2_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_crypto_ikev2_policy(device, "newpolicy")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no crypto ikev2 policy newpolicy"],
        )


if __name__ == "__main__":
    unittest.main()
