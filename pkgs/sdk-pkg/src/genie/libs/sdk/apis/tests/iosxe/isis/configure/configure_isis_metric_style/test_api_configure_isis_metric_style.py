import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_metric_style


class TestConfigureIsisMetricStyle(TestCase):

    def test_configure_isis_metric_style(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_metric_style(
            device,
            "wide",
            "level-1",
            "Gi1/0/6",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis",
                "metric-style wide level-1",
                "passive-interface Gi1/0/6",
            ],
        )

    def test_configure_isis_metric_style_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_metric_style(
            device,
            "transition",
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
                "router isis",
                "metric-style transition",
            ],
        )

    def test_configure_isis_metric_style_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_metric_style(
            device,
            "wide",
            None,
            "Gi1/0/6",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis",
                "metric-style wide",
                "passive-interface Gi1/0/6",
            ],
        )

    def test_configure_isis_metric_style_3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_metric_style(
            device,
            "wide",
            "level-1",
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "router isis",
                "metric-style wide level-1",
            ],
        )


if __name__ == "__main__":
    unittest.main()