import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_ppk_on_keyring


class TestUnconfigurePpkOnKeyring(TestCase):

    def test_unconfigure_ppk_on_keyring(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ppk_on_keyring(
            device,
            "HUB-KEY",
            "1",
            "1.1.1.1",
            "0.0.0.0",
            "cisco",
            True,
            "ppk1",
            "cisco123",
            "sks-client-cfg",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 keyring HUB-KEY", sent_commands)
        self.assertIn("peer 1", sent_commands)
        self.assertIn("no address 1.1.1.1 0.0.0.0", sent_commands)
        self.assertIn("no pre-shared-key cisco", sent_commands)
        self.assertIn(
            "no ppk manual id ppk1 key cisco123 required",
            sent_commands,
        )
        self.assertIn(
            "no ppk dynamic sks-client-cfg required",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()