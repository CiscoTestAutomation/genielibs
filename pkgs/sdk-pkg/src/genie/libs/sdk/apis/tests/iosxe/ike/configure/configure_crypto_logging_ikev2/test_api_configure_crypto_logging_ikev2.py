import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_crypto_logging_ikev2


class TestConfigureCryptoLoggingIkev2(TestCase):

    def test_configure_crypto_logging_ikev2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_logging_ikev2(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto logging ikev2", sent_commands)


if __name__ == "__main__":
    unittest.main()