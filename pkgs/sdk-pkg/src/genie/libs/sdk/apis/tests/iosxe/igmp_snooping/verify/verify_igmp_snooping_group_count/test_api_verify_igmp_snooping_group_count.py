import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_snooping_group_count,
)


class TestVerifyIgmpSnoopingGroupCount(unittest.TestCase):

    def test_vlan_within_range(self):
        device = Mock()
        # 'show ip igmp snooping groups vlan 20 count'
        device.api.get_igmp_snooping_groups_count = Mock(
            return_value={'vlan': {'20': {'count': 256}}})

        result = verify_igmp_snooping_group_count(
            device, '20', min_count=100, max_count=300,
            max_time=1, check_interval=1)

        device.api.get_igmp_snooping_groups_count.assert_called_with(
            vlan='20')
        self.assertTrue(result)

    def test_vlan_below_min(self):
        device = Mock()
        device.api.get_igmp_snooping_groups_count = Mock(
            return_value={'vlan': {'20': {'count': 256}}})

        result = verify_igmp_snooping_group_count(
            device, '20', min_count=300, max_count=500,
            max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_total_within_range(self):
        device = Mock()
        # 'show ip igmp snooping groups count'
        device.api.get_igmp_snooping_groups_count = Mock(
            return_value={
                'total_number_of_groups': {'igmp_groups_count': 831}})

        result = verify_igmp_snooping_group_count(
            device, None, min_count=800, max_count=900,
            max_time=1, check_interval=1)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
