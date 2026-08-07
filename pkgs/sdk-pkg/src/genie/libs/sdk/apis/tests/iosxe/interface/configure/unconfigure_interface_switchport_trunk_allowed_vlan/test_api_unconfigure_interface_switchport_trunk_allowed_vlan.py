import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_interface_switchport_trunk_allowed_vlan,
)


class TestUnconfigureInterfaceSwitchportTrunkAllowedVlan(TestCase):

    def test_unconfigure_interface_switchport_trunk_allowed_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_switchport_trunk_allowed_vlan(
            device,
            ["po 10"],
            "10-30,499,777",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface po 10",
            sent_commands,
        )
        self.assertIn(
            "no switchport trunk allowed vlan 10-30,499,777",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()