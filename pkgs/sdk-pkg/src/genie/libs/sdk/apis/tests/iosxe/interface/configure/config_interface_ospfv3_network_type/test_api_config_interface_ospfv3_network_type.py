import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    config_interface_ospfv3_network_type,
)


class TestConfigInterfaceOspfv3NetworkType(TestCase):

    def test_config_interface_ospfv3_network_type_ipv6(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_network_type(
            device,
            "vmi1",
            "1",
            "point-to-point",
            "ipv6",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("interface vmi1", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv6 network point-to-point",
            sent_commands,
        )

    def test_config_interface_ospfv3_network_type_ipv4(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_network_type(
            device,
            "vmi1",
            "1",
            "point-to-point",
            "ipv4",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("interface vmi1", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv4 network point-to-point",
            sent_commands,
        )

    def test_config_interface_ospfv3_network_type_both(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_network_type(
            device,
            "vmi1",
            "1",
            "point-to-point",
            "both",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("interface vmi1", sent_commands)
        self.assertIn(
            "ospfv3 1 network point-to-point",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()