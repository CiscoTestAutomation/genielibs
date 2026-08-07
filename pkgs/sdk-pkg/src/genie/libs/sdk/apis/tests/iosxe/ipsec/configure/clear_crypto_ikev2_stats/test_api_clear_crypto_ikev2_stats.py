import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import clear_crypto_ikev2_stats


class TestClearCryptoIkev2Stats(TestCase):

    def test_clear_crypto_ikev2_stats(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = "Cleared crypto ikev2 statistics"

        result = clear_crypto_ikev2_stats(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "clear crypto ikev2 stats",
        )


if __name__ == "__main__":
    unittest.main()