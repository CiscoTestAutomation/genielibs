import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    config_mka_keychain_on_interface,
)


class TestConfigMkaKeychainOnInterface(TestCase):

    def test_config_mka_keychain_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_mka_keychain_on_interface(
            device=device,
            interface="TwentyFiveGigE 1/0/7",
            key_string="mss",
            key_chain="fss",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE 1/0/7",
                "mka pre-shared-key key-chain mss fallback-key-chain fss",
            ],
        )


if __name__ == "__main__":
    unittest.main()
