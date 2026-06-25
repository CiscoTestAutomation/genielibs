import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_power_inline


class TestConfigurePowerInline(TestCase):

    def test_configure_power_inline(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "auto",
            "",
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline auto",
        )

    def test_configure_power_inline_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "auto",
            "",
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline auto",
        )

    def test_configure_power_inline_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "police",
            "",
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline police",
        )

    def test_configure_power_inline_3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "never",
            "",
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline never",
        )

    def test_configure_power_inline_4(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "police",
            "",
            "log",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline police action log",
        )

    def test_configure_power_inline_5(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "police",
            "",
            "errdisable",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline police action errdisable",
        )

    def test_configure_power_inline_6(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "consumption",
            4000,
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline consumption 4000",
        )

    def test_configure_power_inline_7(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "port",
            "",
            "",
            "perpetual-poe-ha",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline port perpetual-poe-ha",
        )

    def test_configure_power_inline_8(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "port",
            "",
            "",
            "1-event",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline port 1-event",
        )

    def test_configure_power_inline_9(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "static",
            4000,
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline static max 4000",
        )

    def test_configure_power_inline_10(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_inline(
            device,
            "Gi1/0/1",
            "auto",
            4000,
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "interface Gi1/0/1\npower inline auto max 4000",
        )


if __name__ == "__main__":
    unittest.main()