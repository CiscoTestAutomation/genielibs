import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    unconfigure_mac_address_table_aging_time_vlan,
)


class TestUnconfigureMacAddressTableAgingTimeVlan(TestCase):

    def test_unconfigure_mac_address_table_aging_time_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mac_address_table_aging_time_vlan(
            device,
            30,
            2,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "no mac-address-table aging-time 30 vlan 2",
            ],
        )


if __name__ == "__main__":
    unittest.main()
