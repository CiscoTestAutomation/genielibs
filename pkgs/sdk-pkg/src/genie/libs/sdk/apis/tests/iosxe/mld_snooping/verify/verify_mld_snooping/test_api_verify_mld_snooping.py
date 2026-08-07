import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.verify import (
    verify_mld_snooping,
)


# parsed output of 'show ipv6 mld snooping vlan 20'
VLAN_PARSED = {
    'mldv2': 'Enabled',
    'suppression': 'Enabled',
    'solicit_query': 'Disabled',
    'flood_query': 2,
    'robustness': 2,
    'query_count': 2,
    'query_interval': 1000,
    'vlan': {
        '20': {
            'mld_leave': 'Disabled',
            'robustness': 2,
            'query_count': 2,
            'query_interval': 1000,
        }
    },
}

# parsed output of 'show ipv6 mld snooping' (global scope)
GLOBAL_PARSED = {
    'mld': 'Enabled',
    'mldv2': 'Enabled',
    'suppression': 'Disabled',
    'robustness': 2,
    'query_count': 2,
    'query_interval': 1000,
}


class TestVerifyMldSnooping(unittest.TestCase):

    def test_verify_vlan_pass(self):
        device = Mock()
        device.api.get_mld_snooping = Mock(return_value=VLAN_PARSED)

        result = verify_mld_snooping(
            device, 20, verify_scope='vlan',
            mld_immediate_leave='Disabled', robustness_variable=2,
            last_listener_query_count=2,
            last_listener_query_interval=1000)

        device.api.get_mld_snooping.assert_called_with(vlan=20)
        self.assertTrue(result)

    def test_verify_vlan_mismatch(self):
        device = Mock()
        device.api.get_mld_snooping = Mock(return_value=VLAN_PARSED)

        result = verify_mld_snooping(
            device, 20, verify_scope='vlan',
            mld_immediate_leave='Enabled')

        self.assertFalse(result)

    def test_verify_global_pass(self):
        device = Mock()
        device.api.get_mld_snooping = Mock(return_value=GLOBAL_PARSED)

        result = verify_mld_snooping(
            device, None, verify_scope='global',
            mld_snooping='Enabled', mldv2_snooping='Enabled',
            listener_message_suppression='Disabled')

        self.assertTrue(result)

    def test_verify_empty(self):
        device = Mock()
        device.api.get_mld_snooping = Mock(return_value={})

        result = verify_mld_snooping(
            device, 20, verify_scope='vlan',
            mld_immediate_leave='Disabled')

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
