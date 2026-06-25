import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_subinterface_action,
    configure_subinterface,
)


class TestConfigureSubinterface(TestCase):

    def test_configure_subinterface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_subinterface(
            device,
            "Te1/0/5",
            "301",
            "172.32.24.1",
            "255.255.255.252",
            "native",
            "FACTORY_VRF",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Te1/0/5.301",
                "encapsulation dot1q 301 native",
                "vrf forwarding FACTORY_VRF",
                "ip address 172.32.24.1 255.255.255.252",
            ],
        )

    def test_configure_interface_subinterface_action(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_subinterface_action(
            device,
            "GigabitEthernet0/1",
            "10",
            "description Uplink_To_DataCenter",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1.10",
                "description Uplink_To_DataCenter",
            ],
        )

    def test_configure_interface_subinterface_action_without_subcommand(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_subinterface_action(
            device,
            "uut",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface uut.1",
            ],
        )


if __name__ == "__main__":
    unittest.main()