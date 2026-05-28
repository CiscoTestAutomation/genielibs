import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_interfaces_on_port_channel,
)


class TestConfigureInterfaceInterfacesOnPortChannel(TestCase):

    def test_configure_interface_interfaces_on_port_channel(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_interfaces_on_port_channel(
            device,
            "g1/0/13",
            "desirable",
            10,
            ["g1/0/13", "g4/0/25", "g4/0/37"],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface g1/0/13", sent_commands)
        self.assertIn("no shutdown", sent_commands)
        self.assertIn("channel-group 10 mode desirable", sent_commands)


if __name__ == "__main__":
    unittest.main()