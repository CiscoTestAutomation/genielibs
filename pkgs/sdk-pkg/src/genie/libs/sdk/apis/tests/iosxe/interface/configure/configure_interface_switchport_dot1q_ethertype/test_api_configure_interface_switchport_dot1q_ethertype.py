import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_switchport_dot1q_ethertype,
)


class TestConfigureInterfaceSwitchportDot1qEthertype(TestCase):

    def test_configure_interface_switchport_dot1q_ethertype(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_switchport_dot1q_ethertype(
            device,
            "HundredGigE1/0/4",
            "88a8",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface HundredGigE1/0/4", sent_commands)
        self.assertIn("switchport dot1q ethertype 88a8", sent_commands)


if __name__ == "__main__":
    unittest.main()