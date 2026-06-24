import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_switchport_pvlan_mode,
)


class TestConfigureInterfaceSwitchportPvlanMode(TestCase):

    def test_configure_interface_switchport_pvlan_mode(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_switchport_pvlan_mode(
            device=device,
            interface="GigabitEthernet1/0/11",
            mode="host",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/11", sent_commands)
        self.assertIn("switchport mode private-vlan host", sent_commands)


if __name__ == "__main__":
    unittest.main()