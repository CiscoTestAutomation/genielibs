import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_interface_ospfv3_cost


class TestUnconfigInterfaceOspfv3Cost(TestCase):

    def test_unconfig_interface_ospfv3_cost(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_cost(
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
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1/0",
                "no ospfv3 1 ipv6 cost dynamic hysteresis percent 100",
            ],
        )

    def test_unconfig_interface_ospfv3_cost_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_cost(
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
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1/0",
                "no ospfv3 1 ipv6 cost dynamic hysteresis threshold 10",
            ],
        )

    def test_unconfig_interface_ospfv3_cost_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_cost(
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
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1/0",
                "no ospfv3 1 ipv6 cost dynamic weight throughput 50",
            ],
        )

    def test_unconfig_interface_ospfv3_cost_3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_cost(
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
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1/0",
                "no ospfv3 1 ipv6 cost dynamic weight resources 40",
            ],
        )

    def test_unconfig_interface_ospfv3_cost_4(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_cost(
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
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1/0",
                "no ospfv3 1 ipv6 cost dynamic weight latency 30",
            ],
        )

    def test_unconfig_interface_ospfv3_cost_5(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_cost(
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
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1/0",
                "no ospfv3 1 ipv6 cost dynamic weight l2-factor 20",
            ],
        )

    def test_unconfig_interface_ospfv3_cost_6(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3_cost(
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
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/1/0",
                "no ospfv3 1 ipv6 cost dynamic",
            ],
        )


if __name__ == "__main__":
    unittest.main()