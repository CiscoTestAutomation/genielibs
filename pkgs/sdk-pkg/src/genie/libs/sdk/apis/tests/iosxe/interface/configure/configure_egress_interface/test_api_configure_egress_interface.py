import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_egress_interface


class TestConfigureEgressInterface(TestCase):

    def test_configure_egress_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_egress_interface(
            device,
            {"GigabitEthernet1/0/17": None},
            "90",
            "1-4094",
            "1222",
            "222",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/17", sent_commands)
        self.assertIn("switchport mode private-vlan trunk", sent_commands)
        self.assertIn("switchport trunk native vlan 90", sent_commands)
        self.assertIn(
            "switchport private-vlan trunk allowed vlan 1-4094",
            sent_commands,
        )
        self.assertIn(
            "switchport private-vlan association trunk 1222 222",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()