import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_vrf_snooping_group,
)


# parsed output of 'show ip igmp vrf vrf_test snooping groups'
PARSED = {
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

# entry with multiple ports to verify order-independent comparison
PARSED_MULTI_PORT = {
    '1': {
        'vlan': 20,
        'group': '224.1.1.1',
        'type': 'I',
        'version': 'v2',
        'port_list': ['GigabitEthernet0/1/5', 'GigabitEthernet0/1/6'],
    },
}


class TestVerifyIgmpVrfSnoopingGroup(unittest.TestCase):

    def test_pass(self):
        device = Mock()
        device.api.get_igmp_vrf_snooping_groups = Mock(
            return_value=PARSED)

        result = verify_igmp_vrf_snooping_group(
            device, 'vrf_test', 20, '224.1.1.1', 'I', 'v2',
            ['GigabitEthernet0/1/6'], max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_port_order(self):
        device = Mock()
        device.api.get_igmp_vrf_snooping_groups = Mock(
            return_value=PARSED_MULTI_PORT)

        # Expected port_list given in a different order than parsed entry
        result = verify_igmp_vrf_snooping_group(
            device, 'vrf_test', 20, '224.1.1.1', 'I', 'v2',
            ['GigabitEthernet0/1/6', 'GigabitEthernet0/1/5'],
            max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_mismatch(self):
        device = Mock()
        device.api.get_igmp_vrf_snooping_groups = Mock(
            return_value=PARSED)

        result = verify_igmp_vrf_snooping_group(
            device, 'vrf_test', 20, '224.1.1.1', 'I', 'v3',
            ['GigabitEthernet0/1/6'], max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_empty(self):
        device = Mock()
        device.api.get_igmp_vrf_snooping_groups = Mock(return_value={})

        result = verify_igmp_vrf_snooping_group(
            device, 'vrf_test', 20, '224.1.1.1', 'I', 'v2',
            ['GigabitEthernet0/1/6'], max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
