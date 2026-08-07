import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_group,
)


# parsed output of 'show ip igmp groups'
PARSED = {
    'igmp_groups': {
        '228.0.8.204': {
            'intf': 'Vlan10',
            'uptime': '00:02:26',
            'expires': '00:02:45',
            'last_reporter': '60.1.1.2',
        },
    },
}


class TestVerifyIgmpGroup(unittest.TestCase):

    def test_pass(self):
        device = Mock()
        device.api.get_igmp_groups = Mock(return_value=PARSED)

        result = verify_igmp_group(
            device, '228.0.8.204', 'Vlan10',
            last_reporter='60.1.1.2', max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_pass_shorthand_interface(self):
        device = Mock()
        parsed = {
            'igmp_groups': {
                '228.0.8.204': {
                    'intf': 'GigabitEthernet0/1/7',
                    'last_reporter': '60.1.1.2',
                },
            },
        }
        device.api.get_igmp_groups = Mock(return_value=parsed)

        # caller passes shorthand alias, device returns full name
        result = verify_igmp_group(
            device, '228.0.8.204', 'Gi0/1/7',
            max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_not_found(self):
        device = Mock()
        device.api.get_igmp_groups = Mock(return_value=PARSED)

        result = verify_igmp_group(
            device, '239.9.9.9', 'Vlan10',
            max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_empty(self):
        device = Mock()
        device.api.get_igmp_groups = Mock(return_value={})

        result = verify_igmp_group(
            device, '228.0.8.204', 'Vlan10',
            max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
