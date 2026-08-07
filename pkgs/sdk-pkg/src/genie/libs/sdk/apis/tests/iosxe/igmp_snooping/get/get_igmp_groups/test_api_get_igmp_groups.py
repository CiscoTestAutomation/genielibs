import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.igmp_snooping.get import (
    get_igmp_groups,
)


class TestGetIgmpGroups(unittest.TestCase):

    # parsed output of:
    #    show ip igmp groups
    #    Group Address  Interface Uptime    Expires   Last Reporter
    #    228.0.8.204    Vlan10    00:02:26  00:02:45  60.1.1.2
    parsed = {
        'igmp_groups': {
            '228.0.8.204': {
                'intf': 'Vlan10',
                'uptime': '00:02:26',
                'expires': '00:02:45',
                'last_reporter': '60.1.1.2',
            },
        },
    }

    def test_get_igmp_groups(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_igmp_groups(device)
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with('show ip igmp groups')

    def test_get_igmp_groups_interface(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_igmp_groups(device, interface='Vlan10')
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with(
            'show ip igmp groups Vlan10')

    def test_get_igmp_groups_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_igmp_groups(device)
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
