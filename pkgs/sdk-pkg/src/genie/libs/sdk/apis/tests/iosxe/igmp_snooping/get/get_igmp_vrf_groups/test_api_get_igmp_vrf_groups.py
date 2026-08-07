import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.igmp_snooping.get import (
    get_igmp_vrf_groups,
)


class TestGetIgmpVrfGroups(unittest.TestCase):

    # parsed output of:
    #    show ip igmp vrf vrf_test groups
    #    Group Address   Interface              Uptime    Expires   Last Reporter
    #    224.1.1.1       Vlan20                 00:00:09  00:02:50  50.50.2.2
    #    224.0.1.40      GigabitEthernet0/1/7   00:00:13  00:02:48  50.50.1.1
    parsed = {
        'igmp_group_address': {
            '224.1.1.1': {
                'interface': 'Vlan20',
                'uptime': '00:00:09',
                'expires': '00:02:50',
                'last_reporter': '50.50.2.2',
            },
            '224.0.1.40': {
                'interface': 'GigabitEthernet0/1/7',
                'uptime': '00:00:13',
                'expires': '00:02:48',
                'last_reporter': '50.50.1.1',
            },
        },
    }

    def test_get_igmp_vrf_groups(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_igmp_vrf_groups(device, 'vrf_test')
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with(
            'show ip igmp vrf vrf_test groups')

    def test_get_igmp_vrf_groups_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_igmp_vrf_groups(device, 'vrf_test')
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
