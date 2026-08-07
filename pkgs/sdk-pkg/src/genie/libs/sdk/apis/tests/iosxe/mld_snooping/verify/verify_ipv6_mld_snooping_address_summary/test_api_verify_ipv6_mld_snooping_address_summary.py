import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.verify import (
    verify_ipv6_mld_snooping_address_summary,
)


# parsed 'show ipv6 mld snooping address vlan 30 FF1E::1'
PARSED = {
    'vlan': {
        '30': {
            'group': {
                'FF1E::1': {
                    'type': 'M',
                    'version': 'v2',
                    'port_list': 'Gi1/0/7',
                }
            }
        }
    }
}


class TestVerifyIpv6MldSnoopingAddressSummary(unittest.TestCase):

    def test_pass(self):
        device = Mock()
        device.api.get_ipv6_mld_snooping_address_summary = Mock(
            return_value=PARSED)

        result = verify_ipv6_mld_snooping_address_summary(
            device, 30, 'FF1E::1', snoop_type='M', version='v2',
            port='Gi1/0/7', max_time=1, check_interval=1)

        device.api.get_ipv6_mld_snooping_address_summary \
            .assert_called_with(vlan=30, group='FF1E::1')
        self.assertTrue(result)

    def test_mismatch(self):
        device = Mock()
        device.api.get_ipv6_mld_snooping_address_summary = Mock(
            return_value=PARSED)

        result = verify_ipv6_mld_snooping_address_summary(
            device, 30, 'FF1E::1', snoop_type='M', version='v1',
            max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_empty(self):
        device = Mock()
        device.api.get_ipv6_mld_snooping_address_summary = Mock(
            return_value={})

        result = verify_ipv6_mld_snooping_address_summary(
            device, 30, 'FF1E::1', snoop_type='M',
            max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
