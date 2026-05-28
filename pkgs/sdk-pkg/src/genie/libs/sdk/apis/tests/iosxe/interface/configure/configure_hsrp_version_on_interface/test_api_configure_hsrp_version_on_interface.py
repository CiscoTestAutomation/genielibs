import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_hsrp_version_on_interface,
)


class TestConfigureHsrpVersionOnInterface(TestCase):

    def test_configure_hsrp_version_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_hsrp_version_on_interface(
            device,
            "vlan10",
            2,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface vlan10", sent_commands)
        self.assertIn("standby version 2", sent_commands)


if __name__ == "__main__":
    unittest.main()