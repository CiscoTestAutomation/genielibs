import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_snooping_group_notexist,
)


ENTRY = {
    'vlan': '20',
    'type': 'I',
    'version': 'v2',
    'port_list': 'Gi0/1/5 Gi0/1/6',
}


class TestVerifyIgmpSnoopingGroupNotexist(unittest.TestCase):

    def test_not_exist(self):
        device = Mock()
        device.api.get_igmp_snooping_group = Mock(return_value={})

        result = verify_igmp_snooping_group_notexist(
            device, '20', '239.9.9.9', max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_still_exist(self):
        device = Mock()
        device.api.get_igmp_snooping_group = Mock(return_value=ENTRY)

        result = verify_igmp_snooping_group_notexist(
            device, '20', '224.1.1.1', max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
