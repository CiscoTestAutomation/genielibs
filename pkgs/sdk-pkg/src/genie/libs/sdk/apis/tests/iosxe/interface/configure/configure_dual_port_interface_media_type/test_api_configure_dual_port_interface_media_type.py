import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_dual_port_interface_media_type,
)


class TestConfigureDualPortInterfaceMediaType(TestCase):

    def test_configure_dual_port_interface_media_type(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_dual_port_interface_media_type(
            device,
            "GigabitEthernet1/4",
            "sfp",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/4", sent_commands)
        self.assertIn("media-type sfp", sent_commands)


if __name__ == "__main__":
    unittest.main()