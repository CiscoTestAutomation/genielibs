import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_bandwidth,
)


class TestConfigureInterfaceBandwidth(TestCase):

    def test_configure_interface_bandwidth(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_bandwidth(
            device,
            "Port-channel10",
            "30000000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Port-channel10", sent_commands)
        self.assertIn("bandwidth 30000000", sent_commands)


if __name__ == "__main__":
    unittest.main()