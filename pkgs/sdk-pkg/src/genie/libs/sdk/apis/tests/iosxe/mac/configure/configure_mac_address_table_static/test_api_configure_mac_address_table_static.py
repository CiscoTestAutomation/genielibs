import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    configure_mac_address_table_static,
)


class TestConfigureMacAddressTableStatic(TestCase):

    def test_configure_mac_address_table_static(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_mac_address_table_static(
            device,
            "0000.6500.1111",
            "100",
            "Te1/0/5",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "mac address-table static 0000.6500.1111"
            " vlan 100 interface Te1/0/5",
        )


if __name__ == "__main__":
    unittest.main()
