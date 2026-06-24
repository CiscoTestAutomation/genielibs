import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_switchport_trunk,
)


class TestConfigureInterfaceSwitchportTrunk(TestCase):

    def test_configure_interface_switchport_trunk(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_switchport_trunk(
            device,
            ["GigabitEthernet1/0/33"],
            12,
            "add",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("interface GigabitEthernet1/0/33", sent_commands)
        self.assertIn("switchport", sent_commands)
        self.assertIn("switchport mode trunk", sent_commands)
        self.assertIn("switchport trunk allowed vlan add 12", sent_commands)


if __name__ == "__main__":
    unittest.main()