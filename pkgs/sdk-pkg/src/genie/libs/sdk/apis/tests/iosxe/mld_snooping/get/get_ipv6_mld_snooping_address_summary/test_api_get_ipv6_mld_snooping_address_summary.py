import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.get import (
    get_ipv6_mld_snooping_address_summary,
)


class TestGetIpv6MldSnoopingAddressSummary(TestCase):

    def test_get_ipv6_mld_snooping_address_summary(self):
        device = Mock()
        # Parsed 'show ipv6 mld snooping address vlan 30 FF1E::1'
        parsed = {
            "vlan": {
                "30": {
                    "group": {
                        "FF1E::1": {
                            "type": "M",
                            "version": "v2",
                            "port_list": "Gi1/0/7",
                        }
                    }
                }
            }
        }
        device.parse = Mock(return_value=parsed)

        result = get_ipv6_mld_snooping_address_summary(
            device, 30, "FF1E::1")

        device.parse.assert_called_once_with(
            "show ipv6 mld snooping address vlan 30 FF1E::1")
        self.assertEqual(result, parsed)

    def test_get_ipv6_mld_snooping_address_summary_empty(self):
        from genie.metaparser.util.exceptions import SchemaEmptyParserError
        device = Mock()
        device.parse = Mock(side_effect=SchemaEmptyParserError("empty"))

        result = get_ipv6_mld_snooping_address_summary(
            device, 30, "FF1E::1")

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
