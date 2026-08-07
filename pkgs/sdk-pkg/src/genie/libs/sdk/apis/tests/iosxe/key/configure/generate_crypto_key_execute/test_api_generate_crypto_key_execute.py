import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.key.configure import (
    generate_crypto_key_execute,
)


class TestGenerateCryptoKeyExecute(TestCase):

    def test_generate_crypto_key_execute(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = generate_crypto_key_execute(
            device,
            "rsa",
            "515",
        )

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "crypto key generate rsa modulus 515",
        )


if __name__ == "__main__":
    unittest.main()
