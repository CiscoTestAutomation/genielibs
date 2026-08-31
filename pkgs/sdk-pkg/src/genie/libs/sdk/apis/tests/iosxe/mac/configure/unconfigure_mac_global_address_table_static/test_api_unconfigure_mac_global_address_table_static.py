import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    unconfigure_mac_global_address_table_static,
)


class TestUnconfigureMacGlobalAddressTableStatic(TestCase):

    def test_unconfigure_mac_global_address_table_static(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mac_global_address_table_static(
            device,
            "aaaa.aaaa.aaaa",
            10,
            "te1/0/5",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no mac address-table static aaaa.aaaa.aaaa vlan 10 interface te1/0/5",
        )


if __name__ == "__main__":
    unittest.main()
