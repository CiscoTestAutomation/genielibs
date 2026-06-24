import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_uplink_interface


class TestConfigureUplinkInterface(TestCase):

    def test_configure_uplink_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_uplink_interface(
            device,
            {
                "GigabitEthernet1/1/0/1": None,
            },
            "1-4093",
            "1222",
            "222",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/1/0/1",
                "switchport",
                "switchport mode private-vlan trunk promiscuous",
                "switchport private-vlan trunk allowed vlan 1-4093",
                "switchport private-vlan mapping trunk 1222 222",
                "ip dhcp snooping trust",
            ],
        )


if __name__ == "__main__":
    unittest.main()