import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.key.configure import crypto_key_export


class TestCryptoKeyExport(TestCase):

    def test_crypto_key_export(self):
        device = Mock()
        device.state_machine.current_state = "enable"

        expected_output = (
            "crypto key export rsa REKEYRSA pem terminal aes test12345\r\n"
            "% Key name: REKEYRSA\r\n"
            "   Usage: General Purpose Key\r\n"
            "   Key data:\r\n"
            "-----BEGIN PUBLIC KEY-----\r\n"
            "-----END PUBLIC KEY-----\r\n"
            "-----BEGIN RSA PRIVATE KEY-----\r\n"
            "-----END RSA PRIVATE KEY-----\r\n"
        )
        device.configure.return_value = expected_output

        result = crypto_key_export(
            device,
            "rsa",
            "REKEYRSA",
            "terminal",
            "aes",
            "test12345",
            30,
        )

        self.assertEqual(result, expected_output)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["crypto key export rsa REKEYRSA pem terminal aes test12345"],
        )
        self.assertEqual(device.configure.call_args.kwargs.get("timeout"), 30)


if __name__ == "__main__":
    unittest.main()
