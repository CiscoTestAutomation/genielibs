import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_crypto_map


class TestConfigureCryptoMap(TestCase):

    def test_configure_crypto_map(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_map(
            device,
            "test",
            "1",
            "1.1.1.1",
            "10",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto map test 1 ipsec-isakmp",
                "set peer 1.1.1.1",
                "match address 10",
                "set transform-set 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()