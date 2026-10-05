import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9800.configure import (
    configure_wireless_management,
)


class TestConfigureWirelessManagement(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "C9800"
        self.device.management = {
            "wireless": {
                "interface": "Vlan121",
                "physical_interface": "GigabitEthernet2",
                "switchport": "trunk",
                "vlan": 121,
                "auto_negotiate": True,
                "address": {"ipv4": "192.0.2.10/24"},
                "gateway": {"ipv4": "192.0.2.1"},
                "routes": {
                    "ipv4": [{
                        "subnet": "198.51.100.0 255.255.255.0",
                        "next_hop": "192.0.2.1",
                    }],
                },
                "ap_profile": "default-ap-profile",
                "credential_name": "wireless",
            },
        }
        self.device.credentials = {
            "wireless": {
                "username": "admin",
                "password": "Secret12345",
            },
        }

    def test_configures_wireless_management_from_testbed(self):
        result = configure_wireless_management(self.device)

        self.assertIsNone(result)
        self.device.api.configure_interface_switchport_trunk.assert_called_once_with(
            interfaces=["GigabitEthernet2"], vlan_id=121, oper="add"
        )
        self.device.api.unshut_interface.assert_called_once_with(
            interface="GigabitEthernet2"
        )
        self.device.api.config_interface_negotiation.assert_called_once_with(
            interface="GigabitEthernet2"
        )
        self.device.api.configure_management_ip.assert_called_once_with(
            interface="Vlan121",
            address={"ipv4": "192.0.2.10/24"},
            no_switchport=False,
            fallback_to_management_vrf=False,
        )
        self.device.api.configure_management_gateway.assert_called_once_with(
            gateway={"ipv4": "192.0.2.1"}
        )
        self.device.api.configure_management_routes.assert_called_once_with(
            routes={
                "ipv4": [{
                    "subnet": "198.51.100.0 255.255.255.0",
                    "next_hop": "192.0.2.1",
                }],
            }
        )
        self.device.configure.assert_called_once_with([
            "wireless management interface Vlan121",
            "exit",
            "ap profile default-ap-profile",
            "mgmtuser username admin password 0 Secret12345 "
            "secret 0 Secret12345",
        ])

    def test_rejects_interface_vlan_mismatch_before_configuration(self):
        self.device.management["wireless"]["vlan"] = 122

        with self.assertRaisesRegex(
                ValueError, "interface Vlan121 does not match VLAN 122"):
            configure_wireless_management(self.device)

        self.device.api.configure_interface_switchport_trunk.assert_not_called()
        self.device.configure.assert_not_called()

    def test_skips_conflicting_global_wireless_gateway(self):
        self.device.management["gateway"] = {"ipv4": "203.0.113.1"}

        configure_wireless_management(self.device)

        self.device.api.configure_management_gateway.assert_not_called()
        self.device.api.configure_management_routes.assert_called_once()

    def test_configures_distinct_wireless_gateway_when_management_uses_vrf(self):
        self.device.management.update({
            "gateway": {"ipv4": "203.0.113.1"},
            "vrf": "Mgmt-vrf",
        })

        configure_wireless_management(self.device)

        self.device.api.configure_management_gateway.assert_called_once_with(
            gateway={"ipv4": "192.0.2.1"}
        )


if __name__ == "__main__":
    unittest.main()
