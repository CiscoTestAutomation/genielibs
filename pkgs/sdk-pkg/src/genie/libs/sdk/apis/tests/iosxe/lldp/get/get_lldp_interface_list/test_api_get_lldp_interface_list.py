import unittest
from unittest.mock import Mock
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError, InvalidCommandError)
from genie.libs.sdk.apis.iosxe.lldp.get import get_lldp_interface_list


class TestGetLldpInterfaceList(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_get_lldp_interface_list(self):
        self.device.parse.return_value = {
            'interfaces': {
                'GigabitEthernet1/0/15': {
                    'tx': 'enabled', 'rx': 'enabled',
                    'tx_state': 'idle', 'rx_state': 'wait for frame',
                },
                'GigabitEthernet1/0/16': {
                    'tx': 'enabled', 'rx': 'enabled',
                    'tx_state': 'idle', 'rx_state': 'wait for frame',
                },
            }
        }
        result = get_lldp_interface_list(self.device)
        self.device.parse.assert_called_once_with('show lldp interface')
        self.device.api.configure_lldp.assert_not_called()
        self.assertEqual(
            sorted(result),
            sorted(['GigabitEthernet1/0/15', 'GigabitEthernet1/0/16']))

    def test_get_lldp_interface_list_empty(self):
        self.device.parse.side_effect = SchemaEmptyParserError("No data")
        result = get_lldp_interface_list(self.device)
        self.assertEqual(result, [])

    def test_get_lldp_interface_list_invalid_command(self):
        self.device.parse.side_effect = InvalidCommandError("Invalid")
        result = get_lldp_interface_list(self.device)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
