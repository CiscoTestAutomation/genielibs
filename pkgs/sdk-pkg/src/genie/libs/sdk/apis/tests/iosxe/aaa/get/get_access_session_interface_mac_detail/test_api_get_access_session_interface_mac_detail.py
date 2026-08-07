import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.sdk.apis.iosxe.aaa.get import (
    get_access_session_interface_mac_detail,
)


# First session MAC of 'show access-session interface
# GigabitEthernet0/1/0 details'
FIRST_MAC = "0030.0000.0001"
MAC_DATA = {
    "ipv6_address": "Unknown",
    "iif_id": "0x09CB0212",
    "ipv4_address": "Unknown",
    "user_name": "auto601",
    "status": "Authorized",
    "domain": "DATA",
    "oper_host_mode": "multi-domain",
    "oper_control_dir": "both",
    "session_timeout": {
        "type": "local",
        "timeout": "100s",
        "remaining": "91s",
    },
    "timeout_action": "Reauthenticate",
    "common_session_id": "1CB1A8C000000168BBA5232B",
    "acct_session_id": "0x00000250",
    "handle": "0x3400011e",
    "current_policy": "dot1x_dvlan_reauth_af",
    "server_policies": {"1": {"vlan_group": {"vlan": 60}}},
    "method_status": {
        "dot1x": {"method": "dot1x", "state": "Authc Success"}
    },
}
PARSED = {
    "interfaces": {
        "GigabitEthernet0/1/0": {
            "mac_address": {
                FIRST_MAC: MAC_DATA,
                "0030.00a0.0022": {
                    "ipv6_address": "Unknown",
                    "iif_id": "0x07FA353B",
                    "ipv4_address": "Unknown",
                    "user_name": "auto1601",
                    "status": "Authorized",
                    "domain": "VOICE",
                    "oper_host_mode": "multi-domain",
                    "oper_control_dir": "both",
                    "session_timeout": {
                        "type": "local",
                        "timeout": "100s",
                        "remaining": "91s",
                    },
                    "timeout_action": "Reauthenticate",
                    "common_session_id": "1CB1A8C000000169BBA71DFF",
                    "acct_session_id": "0x00000251",
                    "handle": "0xfc00011f",
                    "current_policy": "dot1x_dvlan_reauth_af",
                    "server_policies": {
                        "1": {"vlan_group": {"vlan": 160}}
                    },
                    "method_status": {
                        "dot1x": {
                            "method": "dot1x",
                            "state": "Authc Success",
                        }
                    },
                },
            }
        }
    }
}


class TestGetAccessSessionInterfaceMacDetail(unittest.TestCase):

    def test_get_access_session_interface_mac_detail(self):
        device = Mock()
        device.parse = Mock(return_value=PARSED)

        result = get_access_session_interface_mac_detail(
            device, "GigabitEthernet0/1/0", FIRST_MAC)

        device.parse.assert_called_once_with(
            "show access-session interface "
            "GigabitEthernet0/1/0 details")
        self.assertEqual(result, MAC_DATA)

    def test_get_access_session_interface_mac_detail_missing(self):
        device = Mock()
        device.parse = Mock(side_effect=SchemaEmptyParserError("empty"))

        result = get_access_session_interface_mac_detail(
            device, "GigabitEthernet0/1/0", FIRST_MAC)

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
