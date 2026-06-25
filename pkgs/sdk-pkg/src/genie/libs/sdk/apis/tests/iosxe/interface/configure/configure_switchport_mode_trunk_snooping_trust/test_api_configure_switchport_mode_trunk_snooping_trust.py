import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_mode_trunk_snooping_trust


class TestConfigureSwitchportModeTrunkSnoopingTrust(TestCase):

    def test_configure_switchport_mode_trunk_snooping_trust(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_switchport_mode_trunk_snooping_trust(
            device,
            {
                "GigabitEthernet1/0/17": None,
            },
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/17",
                "switchport mode trunk",
                "ip dhcp snooping trust",
            ],
        )


if __name__ == "__main__":
    unittest.main()