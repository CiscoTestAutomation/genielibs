import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.verify import (
    verify_igmp_snooping,
)


# parsed output of 'show ip igmp snooping'
PARSED = {
    'igmp_snooping_oper_state': 'Enabled',
    'igmpv3_snooping': 'Enabled',
    'report_supression': 'Enabled',
    'eht_db_limit': 100000,
    'eht_db_count': 0,
    'tcn_solicit_query': 'Disabled',
    'tcn_flood_query_count': 2,
    'robustness_variable': 2,
    'last_member_query_count': 2,
    'last_member_query_interval': 1000,
    'check_ttl': 'No',
    'check_router_alert_option': 'No',
    'vlan': {
        '1': {
            'igmp_snooping_admin_state': 'Enabled',
            'igmp_snooping_oper_state': 'Enabled',
            'igmpv2_immediate_leave': 'Disabled',
            'explicit_host_tracking': 'Enabled',
            'report_supression': 'Enabled',
            'robustness_variable': 2,
            'last_member_query_count': 2,
            'last_member_query_interval': 1000,
            'eht_db_limit': 100000,
            'eht_db_count': 0,
            'check_ttl': 'Yes',
            'check_router_alert_option': 'Yes',
        },
    },
}


class TestVerifyIgmpSnooping(unittest.TestCase):

    def test_verify_global_pass(self):
        device = Mock()
        device.api.get_igmp_snooping = Mock(return_value=PARSED)

        result = verify_igmp_snooping(
            device,
            igmp_snooping_oper_state='Enabled',
            igmpv3_snooping='Enabled',
            report_supression='Enabled')

        self.assertTrue(result)

    def test_verify_vlan_pass(self):
        device = Mock()
        device.api.get_igmp_snooping = Mock(return_value=PARSED)

        result = verify_igmp_snooping(
            device, vlan='1',
            igmp_snooping_admin_state='Enabled',
            igmp_snooping_oper_state='Enabled',
            check_ttl='Yes',
            check_router_alert_option='Yes')

        self.assertTrue(result)

    def test_verify_vlan_mismatch(self):
        device = Mock()
        device.api.get_igmp_snooping = Mock(return_value=PARSED)

        result = verify_igmp_snooping(
            device, vlan='1',
            igmp_snooping_admin_state='Disabled')

        self.assertFalse(result)

    def test_verify_empty(self):
        device = Mock()
        device.api.get_igmp_snooping = Mock(return_value={})

        result = verify_igmp_snooping(
            device, igmp_snooping_oper_state='Enabled')

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
