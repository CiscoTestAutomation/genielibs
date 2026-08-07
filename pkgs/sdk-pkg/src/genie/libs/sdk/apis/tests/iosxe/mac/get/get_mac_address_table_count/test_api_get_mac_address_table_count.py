import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.mac.get import (
    get_mac_address_table_count,
)


class TestGetMacAddressTableCount(unittest.TestCase):

    def test_get_mac_address_table_count(self):
        device = Mock()
        # parsed output of 'show mac address-table count':
        #    Mac Entries for Vlan 1:
        #    Dynamic Address Count  : 2
        #    Static  Address Count  : 1
        #    Total Mac Addresses    : 3
        #    Total Dynamic Address Count  : 2
        #    Total Static  Address Count  : 1
        #    Total Mac Address In Use     : 3
        parsed = {
            'vlan': {
                '1': {
                    'dynamic_address_count': 2,
                    'static_address_count': 1,
                    'total_mac_address': 3,
                },
            },
            'total_dynamic_address_count': 2,
            'total_static_address_count': 1,
            'total_mac_address_in_use': 3,
        }
        device.parse = Mock(return_value=parsed)
        result = get_mac_address_table_count(device)
        self.assertEqual(result, parsed)
        device.parse.assert_called_once_with(
            'show mac address-table count')

    def test_get_mac_address_table_count_vlan(self):
        device = Mock()
        # parsed output of 'show mac address-table count vlan 1':
        #    Mac Entries for Vlan 1:
        #    Dynamic Address Count  : 2
        #    Static  Address Count  : 1
        #    Total Mac Addresses    : 3
        parsed = {
            'Total_dynamic_address_count': 2,
            'Total_static_address_count': 1,
            'Total_mac_address_in_use': 3,
        }
        device.parse = Mock(return_value=parsed)
        result = get_mac_address_table_count(device, vlan=1)
        self.assertEqual(result, parsed)
        device.parse.assert_called_once_with(
            'show mac address-table count vlan 1')

    def test_get_mac_address_table_count_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_mac_address_table_count(device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
