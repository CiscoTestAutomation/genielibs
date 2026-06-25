import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_crypto_map_on_interface


class TestUnconfigureCryptoMapOnInterface(TestCase):

    def test_unconfigure_crypto_map_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_crypto_map_on_interface(
            device,
            "GigabitEthernet2",
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface GigabitEthernet2\nno crypto map\n",
        )

    def test_unconfigure_crypto_map_on_interface_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_crypto_map_on_interface(
            device,
            "GigabitEthernet4",
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface GigabitEthernet4\nno ipv6 crypto map\n",
        )


if __name__ == "__main__":
    unittest.main()