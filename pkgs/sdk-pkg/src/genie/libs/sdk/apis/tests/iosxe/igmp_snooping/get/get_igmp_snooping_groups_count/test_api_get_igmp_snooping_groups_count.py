import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.igmp_snooping.get import (
    get_igmp_snooping_groups_count,
)


class TestGetIgmpSnoopingGroupsCount(unittest.TestCase):

    # parsed output of:
    #    show ip igmp snooping groups count
    #    Total number of groups:   831
    parsed = {
        'total_number_of_groups': {
            'igmp_groups_count': 831,
        },
    }

    def test_get_igmp_snooping_groups_count(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_igmp_snooping_groups_count(device)
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with(
            'show ip igmp snooping groups count')

    def test_get_igmp_snooping_groups_count_vlan(self):
        device = Mock()
        # parsed output of 'show ip igmp snooping groups vlan 20 count':
        #    Total number of groups in Vlan 20:   256
        parsed = {
            'vlan': {
                '20': {
                    'count': 256,
                },
            },
        }
        device.parse = Mock(return_value=parsed)
        result = get_igmp_snooping_groups_count(device, vlan='20')
        self.assertEqual(result, parsed)
        device.parse.assert_called_once_with(
            'show ip igmp snooping groups vlan 20 count')

    def test_get_igmp_snooping_groups_count_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_igmp_snooping_groups_count(device)
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
