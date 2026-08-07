import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_vrf_snooping_group_notexist,
)


PARSED = {
    '1': {
        'vlan': 20,
        'group': '224.1.1.1',
        'type': 'I',
        'version': 'v2',
        'port_list': ['GigabitEthernet0/1/6'],
    },
}


class TestVerifyIgmpVrfSnoopingGroupNotexist(unittest.TestCase):

    def test_not_exist(self):
        device = Mock()
        device.api.get_igmp_vrf_snooping_groups = Mock(return_value={})

        result = verify_igmp_vrf_snooping_group_notexist(
            device, 'vrf_test', 20, '224.1.1.1',
            max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_still_exist(self):
        device = Mock()
        device.api.get_igmp_vrf_snooping_groups = Mock(
            return_value=PARSED)

        result = verify_igmp_vrf_snooping_group_notexist(
            device, 'vrf_test', 20, '224.1.1.1',
            max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
