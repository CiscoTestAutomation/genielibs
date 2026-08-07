import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.mac.get import (
    get_mac_address_table_aging_time,
)


class TestGetMacAddressTableAgingTime(unittest.TestCase):

    def test_get_mac_address_table_aging_time(self):
        device = Mock()
        parsed = {'mac_aging_time': 300}
        device.parse = Mock(return_value=parsed)
        result = get_mac_address_table_aging_time(device)
        self.assertEqual(result, parsed)
        device.parse.assert_called_once_with(
            'show mac address-table aging-time')

    def test_get_mac_address_table_aging_time_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_mac_address_table_aging_time(device)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
