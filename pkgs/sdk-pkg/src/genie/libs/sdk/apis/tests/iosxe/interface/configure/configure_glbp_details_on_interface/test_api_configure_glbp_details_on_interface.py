import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_glbp_details_on_interface,
)


class TestConfigureGlbpDetailsOnInterface(TestCase):

    def test_configure_glbp_details_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_glbp_details_on_interface(
            device,
            "vlan10",
            0,
            "10.1.0.3",
            None,
            "150",
            "0",
            "1",
            "4",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface vlan10", sent_commands)
        self.assertIn("glbp 0  ip 10.1.0.3", sent_commands)
        self.assertIn("glbp 0  priority 150", sent_commands)
        self.assertIn("glbp 0  preempt delay sync 0", sent_commands)
        self.assertIn("glbp 0 timers 1 4", sent_commands)


if __name__ == "__main__":
    unittest.main()