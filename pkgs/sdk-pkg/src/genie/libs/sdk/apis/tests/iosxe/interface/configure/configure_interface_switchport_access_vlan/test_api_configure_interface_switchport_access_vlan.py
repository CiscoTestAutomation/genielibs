import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_switchport_access_vlan,
)


class TestConfigureInterfaceSwitchportAccessVlan(TestCase):

    def test_configure_interface_switchport_access_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_switchport_access_vlan(
            device,
            "GigabitEthernet0/2/0",
            "10",
            None,
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet0/2/0", sent_commands)
        self.assertIn("switchport access vlan 10", sent_commands)


if __name__ == "__main__":
    unittest.main()