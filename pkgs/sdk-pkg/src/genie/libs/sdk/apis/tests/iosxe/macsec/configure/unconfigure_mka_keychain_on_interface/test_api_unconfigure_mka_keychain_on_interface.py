import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    unconfigure_mka_keychain_on_interface,
)


class TestUnconfigureMkaKeychainOnInterface(TestCase):

    def test_unconfigure_mka_keychain_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mka_keychain_on_interface(
            device,
            "GigabitEthernet1/0/10",
            "kc1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/10",
                "no mka pre-shared-key key-chain kc1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
