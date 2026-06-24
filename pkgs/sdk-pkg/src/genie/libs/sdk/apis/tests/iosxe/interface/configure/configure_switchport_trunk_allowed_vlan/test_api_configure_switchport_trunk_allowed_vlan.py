import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_trunk_allowed_vlan


class TestConfigureSwitchportTrunkAllowedVlan(TestCase):

    def test_configure_switchport_trunk_allowed_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_switchport_trunk_allowed_vlan(
            device,
            "TwoGigabitEthernet1/0/3",
            10,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwoGigabitEthernet1/0/3",
                "switchport",
                "switchport mode trunk",
                "switchport trunk allowed vlan 10",
            ],
        )


if __name__ == "__main__":
    unittest.main()