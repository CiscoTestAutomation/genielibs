import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    configure_crypto_transform_set,
)


class TestConfigureCryptoTransformSet(TestCase):

    def test_configure_crypto_transform_set(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_transform_set(
            device,
            "test_transform_name",
            "esp-aes",
            "esp-sha-hmac",
            "tunnel",
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto ipsec transform-set test_transform_name esp-aes esp-sha-hmac",
                "mode tunnel",
            ],
        )


if __name__ == "__main__":
    unittest.main()