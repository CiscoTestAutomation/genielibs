import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_interface_ospfv3_network_type


class TestUnconfigInterfaceOspfv3NetworkType(TestCase):

    def test_unconfig_interface_ospfv3_network_type_ipv6(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_network_type(
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
        self.assertEqual(
            sent_commands,
            "interface vmi1\nno ospfv3 1 ipv6 network point-to-point",
        )

    def test_unconfig_interface_ospfv3_network_type_ipv4(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_network_type(
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
        self.assertEqual(
            sent_commands,
            "interface vmi1\nno ospfv3 1 ipv4 network point-to-point",
        )

    def test_unconfig_interface_ospfv3_network_type_both(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_network_type(
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
        self.assertEqual(
            sent_commands,
            "interface vmi1\nno ospfv3 1 network point-to-point",
        )


if __name__ == "__main__":
    unittest.main()