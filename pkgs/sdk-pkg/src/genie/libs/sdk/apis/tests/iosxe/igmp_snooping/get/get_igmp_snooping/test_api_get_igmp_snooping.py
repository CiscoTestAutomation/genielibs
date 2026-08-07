import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.igmp_snooping.get import (
    get_igmp_snooping,
)


class TestGetIgmpSnooping(unittest.TestCase):

    # parsed output of:
    #    show ip igmp snooping
    #    Global IGMP Snooping configuration:
    #    IGMP snooping Oper State     : Enabled
    #    IGMPv3 snooping              : Enabled
    #    Report suppression           : Enabled
    #    EHT DB limit/count           : 100000/0
    #    TCN solicit query            : Disabled
    #    TCN flood query count        : 2
    #    Robustness variable          : 2
    #    Last member query count      : 2
    #    Last member query interval   : 1000
    #    Check TTL=1                  : No
    #    Check Router-Alert-Option    : No
    #    Vlan 1:
    #    IGMP snooping Admin State           : Enabled
    #    IGMP snooping Oper State            : Enabled
    #    IGMPv2 immediate leave              : Disabled
    #    Explicit host tracking              : Enabled
    #    Report suppression                  : Enabled
    #    Robustness variable                 : 2
    #    Last member query count             : 2
    #    Last member query interval          : 1000
    #    EHT DB limit/count                  : 100000/0
    #    Check TTL=1                         : Yes
    #    Check Router-Alert-Option           : Yes
    parsed = {
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

    def test_get_igmp_snooping(self):
        device = Mock()
        device.parse = Mock(return_value=self.parsed)
        result = get_igmp_snooping(device)
        self.assertEqual(result, self.parsed)
        device.parse.assert_called_once_with('show ip igmp snooping')

    def test_get_igmp_snooping_empty(self):
        device = Mock()
        device.parse = Mock(
            side_effect=SchemaEmptyParserError('No data'))
        result = get_igmp_snooping(device)
        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
