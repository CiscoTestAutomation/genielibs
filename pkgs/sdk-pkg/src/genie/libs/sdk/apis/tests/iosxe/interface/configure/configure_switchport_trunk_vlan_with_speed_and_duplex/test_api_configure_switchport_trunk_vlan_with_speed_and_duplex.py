import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_switchport_trunk_vlan_with_speed_and_duplex,
)


class TestConfigureSwitchportTrunkVlanWithSpeedAndDuplex(TestCase):

    def test_configure_switchport_trunk_vlan_with_speed_and_duplex(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_switchport_trunk_vlan_with_speed_and_duplex(
            device,
            "GigabitEthernet3/0/25",
            "3",
            "10",
            "full",
            "output",
            "test-shape",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet3/0/25",
                "switchport access vlan 3",
                "switchport mode access",
                "speed 10",
                "duplex full",
                "service-policy output test-shape",
            ],
        )


if __name__ == "__main__":
    unittest.main()