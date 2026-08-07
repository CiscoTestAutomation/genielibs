import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_interface_switchport_pvlan_mapping,
)


class TestUnconfigureInterfaceSwitchportPvlanMapping(TestCase):

    def test_unconfigure_interface_switchport_pvlan_mapping(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_switchport_pvlan_mapping(
            device,
            "TwentyFiveGigE1/0/37",
            "trunk",
            "500",
            "501",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface TwentyFiveGigE1/0/37",
            sent_commands,
        )
        self.assertIn(
            "no switchport private-vlan mapping trunk 500 501",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()