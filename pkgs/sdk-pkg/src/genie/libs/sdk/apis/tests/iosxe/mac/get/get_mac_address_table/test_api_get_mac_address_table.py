import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.mac.get import get_mac_address_table


class TestGetMacAddressTable(unittest.TestCase):

    # parsed output of:
    #    1    0000.0022.2201    DYNAMIC     Gi0/1/6
    #    1    0000.0033.3301    STATIC      Gi0/1/5
    parsed = {
        'mac_table': {
            'vlans': {
                '1': {
                    'vlan': 1,
                    'mac_addresses': {
                        '0000.0022.2201': {
                            'mac_address': '0000.0022.2201',
                            'interfaces': {
                                'GigabitEthernet0/1/6': {
                                    'interface': 'GigabitEthernet0/1/6',
                                    'entry_type': 'dynamic',
                                },
                            },
                        },
                        '0000.0033.3301': {
                            'mac_address': '0000.0033.3301',
                            'interfaces': {
                                'GigabitEthernet0/1/5': {
                                    'interface': 'GigabitEthernet0/1/5',
                                    'entry_type': 'static',
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    def test_get_mac_address_table(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_mac_address_table(device)
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with('show mac address-table')

    def test_get_mac_address_table_interface_vlan(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_mac_address_table(
            device, interface='GigabitEthernet0/1/6', vlan=1)
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with(
            'show mac address-table interface '
            'GigabitEthernet0/1/6 vlan 1')

    def test_get_mac_address_table_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_mac_address_table(device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
