import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.igmp_snooping.get import (
    get_igmp_vrf_snooping_groups,
)


class TestGetIgmpVrfSnoopingGroups(unittest.TestCase):

    # parsed output of:
    #    show ip igmp vrf vrf_test snooping groups
    #    Vlan   Group/source   Type   Version   Port List
    #    20     224.1.1.1      I      v2        Gi0/1/6
    #    30     224.1.1.1      I      v2        Gi0/1/5
    parsed = {
        '1': {
            'vlan': 20,
            'group': '224.1.1.1',
            'type': 'I',
            'version': 'v2',
            'port_list': ['GigabitEthernet0/1/6'],
        },
        '2': {
            'vlan': 30,
            'group': '224.1.1.1',
            'type': 'I',
            'version': 'v2',
            'port_list': ['GigabitEthernet0/1/5'],
        },
    }

    def test_get_igmp_vrf_snooping_groups(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_igmp_vrf_snooping_groups(device, 'vrf_test')
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with(
            'show ip igmp vrf vrf_test snooping groups')

    def test_get_igmp_vrf_snooping_groups_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_igmp_vrf_snooping_groups(device, 'vrf_test')
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
