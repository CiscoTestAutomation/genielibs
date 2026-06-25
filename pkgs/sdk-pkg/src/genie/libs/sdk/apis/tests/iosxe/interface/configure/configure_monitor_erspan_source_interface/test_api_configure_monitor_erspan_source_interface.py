import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_monitor_erspan_source_interface,
)


class TestConfigureMonitorErspanSourceInterface(TestCase):

    def test_configure_monitor_erspan_source_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_monitor_erspan_source_interface(
            device,
            "1",
            "te1/0/2",
            "rx",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("monitor session 1 type erspan-source", sent_commands)
        self.assertIn("source interface te1/0/2 rx", sent_commands)


if __name__ == "__main__":
    unittest.main()