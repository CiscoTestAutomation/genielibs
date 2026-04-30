import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import clear_crypto_session


class TestClearCryptoSession(TestCase):

    def test_clear_crypto_session(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = clear_crypto_session(device, True, False, None, 30)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertIn("clear crypto session active", sent_command)


if __name__ == "__main__":
    unittest.main()