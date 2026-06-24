import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError, InvalidCommandError)
from genie.libs.sdk.apis.iosxe.lldp.get import get_lldp_interface_info


class TestGetLldpInterfaceInfo(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_interface_info(self):
        expected_output = {
            "interfaces": {
                "GigabitEthernet1/0/15": {
                    "tx": "enabled",
                    "rx": "enabled",
                    "tx_state": "idle",
                    "rx_state": "wait for frame",
                },
            }
        }
        self.device.parse.return_value = expected_output
        result = get_lldp_interface_info(self.device, 'GigabitEthernet1/0/15')
        self.device.parse.assert_called_once_with(
            'show lldp interface GigabitEthernet1/0/15')
        self.assertEqual(result, expected_output)

    def test_get_lldp_interface_info_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_interface_info(self.device, 'GigabitEthernet1/0/15')
        self.assertIsNone(result)

    def test_get_lldp_interface_info_invalid_command(self):
        self.device.parse.side_effect = InvalidCommandError("Invalid")
        result = get_lldp_interface_info(self.device, 'GigabitEthernet1/0/15')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
