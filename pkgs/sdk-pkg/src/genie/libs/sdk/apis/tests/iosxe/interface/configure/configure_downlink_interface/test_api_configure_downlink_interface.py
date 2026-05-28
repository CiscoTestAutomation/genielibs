import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_downlink_interface


class TestConfigureDownlinkInterface(TestCase):

    def test_configure_downlink_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_downlink_interface(
            device,
            {"GigabitEthernet1/1/0/25": None},
            "1-4093",
            "1222",
            "222",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/1/0/25", sent_commands)
        self.assertIn("switchport mode private-vlan trunk", sent_commands)
        self.assertIn(
            "switchport private-vlan trunk allowed vlan 1-4093",
            sent_commands,
        )
        self.assertIn(
            "switchport private-vlan association trunk 1222 222",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()