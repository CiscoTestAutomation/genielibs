import unittest
from unittest.mock import Mock

from genie.utils import Dq
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.igmp_snooping.get import (
    get_igmp_snooping_group,
)


class TestGetIgmpSnoopingGroup(unittest.TestCase):

    # parsed output of:
    #    show ip igmp snooping groups vlan 20 224.1.1.1
    #    Flags: I -- IGMP snooping, S -- Static, P -- PIM snooping,
    #           A -- ASM mode, E -- EVPN sync
    #    Vlan   Group/source   Type   Version   Port List
    #    20     224.1.1.1      I      v2        Gi0/1/5 Gi0/1/6
    parsed = {
        'igmp_groups': {
            '224.1.1.1': {
                'vlan': '20',
                'type': 'I',
                'version': 'v2',
                'port_list': 'Gi0/1/5 Gi0/1/6',
            },
        },
    }

    def _device(self, parsed):
        device = Mock()
        out = Mock()
        out.q = Dq(parsed)
        out.__getitem__ = lambda _self, key: parsed[key]
        device.parse = Mock(return_value=out)
        return device

    def test_get_igmp_snooping_group(self):
        device = self._device(self.parsed)
        result = get_igmp_snooping_group(device, '20', '224.1.1.1')
        self.assertEqual(result, {
            'vlan': '20',
            'type': 'I',
            'version': 'v2',
            'port_list': 'Gi0/1/5 Gi0/1/6',
        })
        device.parse.assert_called_once_with(
            'show ip igmp snooping groups vlan 20 224.1.1.1')

    def test_get_igmp_snooping_group_no_match(self):
        device = self._device(self.parsed)
        result = get_igmp_snooping_group(device, '20', '239.9.9.9')
        self.assertEqual(result, {})

    def test_get_igmp_snooping_group_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_igmp_snooping_group(device, '20', '224.1.1.1')
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
