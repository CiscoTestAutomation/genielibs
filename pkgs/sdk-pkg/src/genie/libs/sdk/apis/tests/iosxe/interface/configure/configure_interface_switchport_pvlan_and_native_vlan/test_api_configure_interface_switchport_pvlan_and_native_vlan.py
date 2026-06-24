import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_switchport_pvlan_and_native_vlan,
)


class TestConfigureInterfaceSwitchportPvlanAndNativeVlan(TestCase):

    def test_configure_interface_switchport_pvlan_and_native_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_switchport_pvlan_and_native_vlan(
            device,
            "twentyFiveGigE 1/0/7",
            "trunk",
            "101",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface twentyFiveGigE 1/0/7", sent_commands)
        self.assertIn(
            "switchport private-vlan trunk native vlan 101",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()