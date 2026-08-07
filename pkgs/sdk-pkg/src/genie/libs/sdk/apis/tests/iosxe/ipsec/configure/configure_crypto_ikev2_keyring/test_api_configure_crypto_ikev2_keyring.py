import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    configure_crypto_ikev2_keyring,
)


class TestConfigureCryptoIkev2Keyring(TestCase):

    def test_configure_crypto_ikev2_keyring(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_ikev2_keyring(
            device,
            "key1",
            "peer1",
            "test",
            "1.1.1.1",
            "255.255.255.0",
            "ipv4",
            "1.1.1.1",
            "234",
            "test1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto ikev2 keyring key1",
                "peer peer1",
                "address 1.1.1.1 255.255.255.0",
                "pre-shared-key test",
                "identity address 1.1.1.1",
                "ppk manual id 234 key test1",
            ],
        )


if __name__ == "__main__":
    unittest.main()