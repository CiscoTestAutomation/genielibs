import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.sdk.apis.iosxe.aaa.get import (
    get_show_access_session_mac_detail,
)


class TestGetShowAccessSessionMacDetail(unittest.TestCase):

    def test_get_show_access_session_mac_detail(self):
        device = Mock()
        # Parsed 'show access-session mac 0030.0000.0001 details'
        parsed = {
            "mac": {
                "0030.0000.0001": {
                    "interface": "GigabitEthernet0/1/0",
                    "iif_id": "0x09CB0212",
                    "ipv6_address": "Unknown",
                    "ipv4_address": "Unknown",
                    "user_name": "auto601",
                    "status": "Authorized",
                    "domain": "DATA",
                    "oper_host_mode": "multi-domain",
                    "oper_control_dir": "both",
                    "timeout_action": "Reauthenticate",
                    "common_session_id": "1CB1A8C000000168BBA5232B",
                    "acct_session_id": "0x00000250",
                    "handle": "0x3400011e",
                    "current_policy": "dot1x_dvlan_reauth_af",
                    "server_policies": {"vlan_group": 60},
                    "method_status_list": {
                        "method": "dot1x",
                        "state": "Authc Success",
                    },
                }
            }
        }
        device.parse = Mock(return_value=parsed)

        result = get_show_access_session_mac_detail(
            device, "0030.0000.0001")

        device.parse.assert_called_once_with(
            "show access-session mac 0030.0000.0001 details")
        self.assertEqual(result, parsed)

    def test_get_show_access_session_mac_detail_error(self):
        device = Mock()
        device.parse = Mock(side_effect=SchemaEmptyParserError("empty"))

        result = get_show_access_session_mac_detail(
            device, "0030.0000.0001")

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
