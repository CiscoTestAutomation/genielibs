import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_crypto_map_on_interface,
)


class TestConfigureCryptoMapOnInterface(TestCase):

    def test_configure_crypto_map_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_map_on_interface(
            device,
            "GigabitEthernet2",
            "map_10",
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("interface GigabitEthernet2", sent_commands)
        self.assertIn("crypto map map_10", sent_commands)

    def test_configure_crypto_map_on_interface_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_map_on_interface(
            device,
            "GigabitEthernet4",
            "map_20",
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("interface GigabitEthernet4", sent_commands)
        self.assertIn("ipv6 crypto map map_20", sent_commands)


if __name__ == "__main__":
    unittest.main()