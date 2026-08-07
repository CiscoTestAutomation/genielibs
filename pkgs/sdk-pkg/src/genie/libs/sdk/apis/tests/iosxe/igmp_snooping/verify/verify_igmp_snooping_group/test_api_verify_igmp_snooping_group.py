import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_snooping_group,
)


# parsed entry of 'show ip igmp snooping groups vlan 20 224.1.1.1'
ENTRY = {
    'vlan': '20',
    'type': 'I',
    'version': 'v2',
    'port_list': 'Gi0/1/5 Gi0/1/6',
}


class TestVerifyIgmpSnoopingGroup(unittest.TestCase):

    def test_verify_igmp_snooping_group_pass(self):
        device = Mock()
        device.api.get_igmp_snooping_group = Mock(return_value=ENTRY)

        result = verify_igmp_snooping_group(
            device, '20', '224.1.1.1', 'I', 'v2',
            ['Gi0/1/5', 'Gi0/1/6'], max_time=1, check_interval=1)

        device.api.get_igmp_snooping_group.assert_called_with(
            '20', '224.1.1.1')
        self.assertTrue(result)

    def test_verify_igmp_snooping_group_port_order(self):
        device = Mock()
        device.api.get_igmp_snooping_group = Mock(return_value=ENTRY)

        # Expected port_list given in a different order than ENTRY
        result = verify_igmp_snooping_group(
            device, '20', '224.1.1.1', 'I', 'v2',
            ['Gi0/1/6', 'Gi0/1/5'], max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_verify_igmp_snooping_group_mismatch(self):
        device = Mock()
        device.api.get_igmp_snooping_group = Mock(return_value=ENTRY)

        result = verify_igmp_snooping_group(
            device, '20', '224.1.1.1', 'I', 'v3',
            ['Gi0/1/5', 'Gi0/1/6'], max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_verify_igmp_snooping_group_empty(self):
        device = Mock()
        device.api.get_igmp_snooping_group = Mock(return_value={})

        result = verify_igmp_snooping_group(
            device, '20', '224.1.1.1', 'I', 'v2',
            ['Gi0/1/5', 'Gi0/1/6'], max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
