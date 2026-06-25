import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_trunk_native_vlan


class TestConfigureSwitchportTrunkNativeVlan(TestCase):

    def test_configure_switchport_trunk_native_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_switchport_trunk_native_vlan(
            device,
            {
                "GigabitEthernet1/0/17": None,
            },
            "90",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/17",
                "switchport trunk native vlan 90",
                "switchport mode trunk",
            ],
        )


if __name__ == "__main__":
    unittest.main()