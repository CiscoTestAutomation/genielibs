import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_interface_switchport_port_security,
)


class TestUnconfigureInterfaceSwitchportPortSecurity(TestCase):

    def test_unconfigure_interface_switchport_port_security(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_switchport_port_security(
            device,
            "Gi1/0/5",
            "maximum",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Gi1/0/5",
            sent_commands,
        )
        self.assertIn(
            "no switchport port-security maximum 1",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()