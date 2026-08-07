import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    unconfigure_crypto_ikev2_keyring,
)


class TestUnconfigureCryptoIkev2Keyring(TestCase):

    def test_unconfigure_crypto_ikev2_keyring(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_crypto_ikev2_keyring(device, "test_keyring")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["no crypto ikev2 keyring test_keyring"],
        )


if __name__ == "__main__":
    unittest.main()
