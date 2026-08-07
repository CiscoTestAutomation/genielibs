import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ip_on_interface


class TestUnconfigureIpOnInterface(TestCase):

    def test_unconfigure_ip_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_on_interface(
            device,
            "Gi1/0/7",
            "5.5.5.5",
            "255.255.255.0",
            None,
            "sap",
            None,
            None,
            True,
            "test",
            None,
            None,
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Gi1/0/7",
            sent_commands,
        )
        self.assertIn(
            "no encapsulation sap",
            sent_commands,
        )
        self.assertIn(
            "no ip address dhcp hostname test",
            sent_commands,
        )

    def test_unconfigure_ip_on_interface_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_on_interface(
            device,
            "Gi1/0/7",
            "5.5.5.5",
            "255.255.255.0",
            None,
            None,
            None,
            None,
            True,
            "",
            None,
            None,
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Gi1/0/7",
            sent_commands,
        )
        self.assertIn(
            "no ip address dhcp",
            sent_commands,
        )

    def test_unconfigure_ip_on_interface_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_on_interface(
            device,
            "Gi1/0/7",
            "5.5.5.5",
            "255.255.255.0",
            None,
            "arpa",
            None,
            None,
            False,
            "",
            None,
            None,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Gi1/0/7",
            sent_commands,
        )
        self.assertIn(
            "no encapsulation arpa",
            sent_commands,
        )
        self.assertIn(
            "no ip address 5.5.5.5 255.255.255.0 secondary",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()