import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import remove_interface_ip


class TestRemoveInterfaceIp(TestCase):

    def test_remove_interface_ip(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = remove_interface_ip(
            device,
            interface="Vlan100",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Vlan100",
                "no ip address",
            ],
        )

    def test_remove_interface_ip_secondary(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = remove_interface_ip(
            device,
            interface="Vlan100",
            ip_address="101.101.101.101",
            mask="255.255.0.0",
            secondary=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Vlan100",
                "no ip address 101.101.101.101 255.255.0.0 secondary",
            ],
        )


if __name__ == "__main__":
    unittest.main()