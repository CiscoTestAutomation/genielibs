import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.verify import (
    verify_access_session_removed,
)


INTERFACE = "GigabitEthernet0/1/0"
MAC = "0030.0000.0001"
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


class TestVerifyAccessSessionRemoved(unittest.TestCase):

    def test_session_removed(self):
        device = Mock()
        device.api.get_access_session_interface_mac_detail = Mock(
            return_value={})

        result = verify_access_session_removed(
            device, MAC, INTERFACE, max_time=1, check_interval=1)

        device.api.get_access_session_interface_mac_detail \
            .assert_called_with(interface=INTERFACE, mac=MAC)
        self.assertTrue(result)

    def test_session_not_removed(self):
        device = Mock()
        device.api.get_access_session_interface_mac_detail = Mock(
            return_value=MAC_DATA)

        result = verify_access_session_removed(
            device, MAC, INTERFACE, max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
