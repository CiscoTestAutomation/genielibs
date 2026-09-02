import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    unconfigure_mac_address_table_control_packet_learn,
)


class TestUnconfigureMacAddressTableControlPacketLearn(TestCase):

    def test_unconfigure_mac_address_table_control_packet_learn(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mac_address_table_control_packet_learn(
            device,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no mac address-table control-packet-learn",
        )


if __name__ == "__main__":
    unittest.main()
