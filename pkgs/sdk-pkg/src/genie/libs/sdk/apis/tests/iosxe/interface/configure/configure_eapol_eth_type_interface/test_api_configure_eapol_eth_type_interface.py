import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_eapol_eth_type_interface,
)


class TestConfigureEapolEthTypeInterface(TestCase):

    def test_configure_eapol_eth_type_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_eapol_eth_type_interface(
            device,
            "GigabitEthernet1/0/10",
            "876F",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/10", sent_commands)
        self.assertIn("eapol eth-type 876F", sent_commands)


if __name__ == "__main__":
    unittest.main()