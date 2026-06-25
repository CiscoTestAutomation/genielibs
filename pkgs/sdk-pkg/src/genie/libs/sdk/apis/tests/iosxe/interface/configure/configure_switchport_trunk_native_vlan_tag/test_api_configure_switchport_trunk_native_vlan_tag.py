import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_trunk_native_vlan_tag


class TestConfigureSwitchportTrunkNativeVlanTag(TestCase):

    def test_configure_switchport_trunk_native_vlan_tag(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_switchport_trunk_native_vlan_tag(
            device,
            "GigabitEthernet1/0/10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/10",
                "switchport trunk native vlan tag",
            ],
        )


if __name__ == "__main__":
    unittest.main()