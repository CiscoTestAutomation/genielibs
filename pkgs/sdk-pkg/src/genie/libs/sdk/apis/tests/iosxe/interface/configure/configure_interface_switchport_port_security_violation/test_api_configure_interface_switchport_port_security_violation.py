import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_switchport_port_security_violation,
)


class TestConfigureInterfaceSwitchportPortSecurityViolation(TestCase):

    def test_configure_interface_switchport_port_security_violation(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_switchport_port_security_violation(
            device,
            "GigabitEthernet2/0/3",
            "protect",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet2/0/3", sent_commands)
        self.assertIn(
            "switchport port-security violation protect",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()