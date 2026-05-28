import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_dot1q_ethertype,
)


class TestConfigureInterfaceDot1qEthertype(TestCase):

    def test_configure_interface_dot1q_ethertype(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_dot1q_ethertype(
            device,
            "GigabitEthernet0/0/0",
            "0x88A8",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/0/0", sent_commands)
        self.assertIn("dot1q tunneling ethertype 0x88A8", sent_commands)


if __name__ == "__main__":
    unittest.main()