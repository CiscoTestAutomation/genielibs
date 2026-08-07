import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.get import get_mld_snooping


class TestGetMldSnooping(TestCase):

    def test_get_mld_snooping(self):
        device = Mock()
        parsed = {
            "global_mld_snooping_configuration": {
                "mld_snooping": "Enabled",
                "global_pim_snooping": "Disabled",
                "mldv2_snooping": "Enabled",
                "listener_message_suppression": "Disabled",
                "tcn_solicit_query": "Disabled",
                "tcn_flood_query_count": "2",
                "robustness_variable": "2",
                "last_listener_query_count": "2",
                "last_listener_query_interval": "1000",
            },
            "vlans": {
                "vlan_1": {
                    "mld_snooping": "Disabled",
                    "robustness_variable": "2",
                    "last_listener_query_count": "2",
                    "last_listener_query_interval": "1000",
                    "pim_snooping": "Disabled",
                    "mld_immediate_leave": "Disabled",
                }
            },
        }
        device.parse = Mock(return_value=parsed)

        result = get_mld_snooping(device)

        device.parse.assert_called_once_with("show ipv6 mld snooping")
        self.assertEqual(result, parsed)

    def test_get_mld_snooping_vlan(self):
        device = Mock()
        # Parsed output of 'show ipv6 mld snooping vlan 20'
        parsed = {
            "mldv2": "Enabled",
            "suppression": "Enabled",
            "solicit_query": "Disabled",
            "flood_query": 2,
            "robustness": 2,
            "query_count": 2,
            "query_interval": 1000,
            "vlan": {
                "20": {
                    "mld_leave": "Disabled",
                    "robustness": 2,
                    "query_count": 2,
                    "query_interval": 1000,
                }
            },
        }
        device.parse = Mock(return_value=parsed)

        result = get_mld_snooping(device, vlan=20)

        device.parse.assert_called_once_with(
            "show ipv6 mld snooping vlan 20")
        self.assertEqual(result, parsed)

    def test_get_mld_snooping_empty(self):
        from genie.metaparser.util.exceptions import SchemaEmptyParserError
        device = Mock()
        device.parse = Mock(side_effect=SchemaEmptyParserError("empty"))

        result = get_mld_snooping(device)

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
