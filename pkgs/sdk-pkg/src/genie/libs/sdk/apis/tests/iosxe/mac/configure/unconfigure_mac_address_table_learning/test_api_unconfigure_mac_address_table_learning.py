import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    unconfigure_mac_address_table_learning,
)


class TestUnconfigureMacAddressTableLearning(TestCase):

    def test_unconfigure_mac_address_table_learning(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mac_address_table_learning(
            device,
            11,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no mac address-table learning vlan 11",
        )


if __name__ == "__main__":
    unittest.main()
