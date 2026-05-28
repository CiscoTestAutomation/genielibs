import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    config_interface_ospfv3_cost,
)


class TestConfigInterfaceOspfv3Cost(TestCase):

    def test_config_interface_ospfv3_cost(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_cost(
            device,
            "GigabitEthernet0/1/0",
            "1",
            "100",
            None,
            None,
            None,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/1/0", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv6 cost dynamic hysteresis percent 100",
            sent_commands,
        )

    def test_config_interface_ospfv3_cost_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_cost(
            device,
            "GigabitEthernet0/1/0",
            "1",
            None,
            "10",
            None,
            None,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/1/0", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv6 cost dynamic hysteresis threshold 10",
            sent_commands,
        )

    def test_config_interface_ospfv3_cost_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_cost(
            device,
            "GigabitEthernet0/1/0",
            "1",
            None,
            None,
            "50",
            None,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/1/0", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv6 cost dynamic weight throughput 50",
            sent_commands,
        )

    def test_config_interface_ospfv3_cost_3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_cost(
            device,
            "GigabitEthernet0/1/0",
            "1",
            None,
            None,
            None,
            "40",
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/1/0", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv6 cost dynamic weight resources 40",
            sent_commands,
        )

    def test_config_interface_ospfv3_cost_4(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_cost(
            device,
            "GigabitEthernet0/1/0",
            "1",
            None,
            None,
            None,
            None,
            "30",
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/1/0", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv6 cost dynamic weight latency 30",
            sent_commands,
        )

    def test_config_interface_ospfv3_cost_5(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_cost(
            device,
            "GigabitEthernet0/1/0",
            "1",
            None,
            None,
            None,
            None,
            None,
            "20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/1/0", sent_commands)
        self.assertIn(
            "ospfv3 1 ipv6 cost dynamic weight l2-factor 20",
            sent_commands,
        )

    def test_config_interface_ospfv3_cost_6(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_interface_ospfv3_cost(
            device,
            "GigabitEthernet0/1/0",
            "1",
            None,
            None,
            None,
            None,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/1/0", sent_commands)
        self.assertIn("ospfv3 1 ipv6 cost dynamic", sent_commands)


if __name__ == "__main__":
    unittest.main()