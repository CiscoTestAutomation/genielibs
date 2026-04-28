import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import disable_crypto_engine_compliance


class TestDisableCryptoEngineCompliance(TestCase):

    def test_disable_crypto_engine_compliance(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = disable_crypto_engine_compliance(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto engine compliance shield disable", sent_commands)


if __name__ == "__main__":
    unittest.main()