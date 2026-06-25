import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_span_cost


class TestConfigureInterfaceSpanCost(TestCase):

    def test_configure_interface_span_cost(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_span_cost(
            device,
            "Tw1/0/10",
            500,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Tw1/0/10", sent_commands)
        self.assertIn("spanning-tree cost 500", sent_commands)

    def test_configure_interface_span_cost_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_span_cost(
            device,
            "Tw1/0/10",
            10,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Tw1/0/10", sent_commands)
        self.assertIn("spanning-tree cost 10", sent_commands)


if __name__ == "__main__":
    unittest.main()