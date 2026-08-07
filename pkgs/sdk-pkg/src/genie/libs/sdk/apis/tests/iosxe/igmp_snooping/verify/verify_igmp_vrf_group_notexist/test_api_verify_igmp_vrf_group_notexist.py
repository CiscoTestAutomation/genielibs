import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_vrf_group_notexist,
)


PARSED = {
    'igmp_group_address': {
        '224.1.1.1': {
            'interface': 'Vlan20',
            'uptime': '00:00:09',
            'expires': '00:02:50',
            'last_reporter': '50.50.2.2',
        },
    },
}


class TestVerifyIgmpVrfGroupNotexist(unittest.TestCase):

    def test_not_exist(self):
        device = Mock()
        device.api.get_igmp_vrf_groups = Mock(return_value=PARSED)

        result = verify_igmp_vrf_group_notexist(
            device, 'vrf_test', '239.9.9.9', 'Vlan20',
            max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_empty(self):
        device = Mock()
        device.api.get_igmp_vrf_groups = Mock(return_value={})

        result = verify_igmp_vrf_group_notexist(
            device, 'vrf_test', '224.1.1.1', 'Vlan20',
            max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_still_exist(self):
        device = Mock()
        device.api.get_igmp_vrf_groups = Mock(return_value=PARSED)

        result = verify_igmp_vrf_group_notexist(
            device, 'vrf_test', '224.1.1.1', 'Vlan20',
            max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_still_exist_shorthand_interface(self):
        device = Mock()
        parsed = {
            'igmp_group_address': {
                '224.1.1.1': {
                    'interface': 'GigabitEthernet0/1/7',
                    'last_reporter': '50.50.2.2',
                },
            },
        }
        device.api.get_igmp_vrf_groups = Mock(return_value=parsed)

        # shorthand alias matches full name, so entry still exists
        result = verify_igmp_vrf_group_notexist(
            device, 'vrf_test', '224.1.1.1', 'Gi0/1/7',
            max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
