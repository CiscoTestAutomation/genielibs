import logging
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, call, patch

from genie.abstract import Lookup
import genie.libs.clean as clean
from genie.libs.clean.stages.iosxe.cat9k.c9800.stages import (
    ConfigureWirelessManagement,
)


logging.disable(logging.CRITICAL)


class _Step:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def failed(self, message, **kwargs):
        raise RuntimeError(message)


class _Steps:
    def start(self, *args, **kwargs):
        return _Step()


class _OneAttemptTimeout:
    def __init__(self, *args, **kwargs):
        self.attempted = False

    def iterate(self):
        if self.attempted:
            return False
        self.attempted = True
        return True

    def sleep(self):
        pass


class _StageSkipped(Exception):
    pass


class TestConfigureWirelessManagement(unittest.TestCase):

    def setUp(self):
        self.wireless = {
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
        }
        self.api = SimpleNamespace(configure_wireless_management=Mock())
        self.device = SimpleNamespace(
            name="C9800",
            management={"wireless": self.wireless},
            api=self.api,
        )
        self.stage = ConfigureWirelessManagement()

    def test_configure_uses_testbed_values(self):
        self.stage.configure_wireless_management(self.device, _Steps())

        self.api.configure_wireless_management.assert_called_once_with(
            interface="Vlan121",
            physical_interface="GigabitEthernet2",
            switchport="trunk",
            vlan=121,
            auto_negotiate=True,
            address={"ipv4": "192.0.2.10/24"},
            gateway={"ipv4": "192.0.2.1"},
            routes=self.wireless["routes"],
            ap_profile="default-ap-profile",
            credential_name="wireless",
        )

    def test_configure_passes_optional_values_as_none(self):
        self.device.management = {
            "wireless": {
                "interface": "Vlan121",
                "address": {"ipv4": "192.0.2.10/24"},
            },
        }

        self.stage.configure_wireless_management(self.device, _Steps())

        self.api.configure_wireless_management.assert_called_once_with(
            interface="Vlan121",
            physical_interface=None,
            switchport=None,
            vlan=None,
            auto_negotiate=None,
            address={"ipv4": "192.0.2.10/24"},
            gateway=None,
            routes=None,
            ap_profile=None,
            credential_name=None,
        )

    def test_configure_skips_without_wireless_management_values(self):
        self.device.management = {}
        self.stage.skipped = Mock(side_effect=_StageSkipped)

        with self.assertRaises(_StageSkipped):
            self.stage.configure_wireless_management(self.device, _Steps())

        self.stage.skipped.assert_called_once_with(
            "Wireless management values are not provided in the Clean or "
            "testbed YAML. Skipping wireless management configuration."
        )
        self.api.configure_wireless_management.assert_not_called()

    def test_configure_reports_conditionally_required_values(self):
        self.device.management = {
            "wireless": {
                "interface": "Vlan121",
                "switchport": "trunk",
            },
        }

        with self.assertRaisesRegex(
                RuntimeError,
                "Missing required wireless management values.*"
                "physical_interface, vlan"):
            self.stage.configure_wireless_management(self.device, _Steps())

        self.api.configure_wireless_management.assert_not_called()

    def test_verify_wireless_management(self):
        self.device.management["wireless"]["address"] = {
            "ipv4": ["192.0.2.10/24", "192.0.2.11/24"],
        }

        def parse(command):
            if command == "show interfaces GigabitEthernet2 trunk":
                return {
                    "interface": {
                        "GigabitEthernet2": {
                            "status": "trunking",
                            "vlans_allowed_active_in_mgmt_domain": "1,100-150",
                            "vlans_in_stp_forwarding_not_pruned": "121",
                        },
                    },
                }
            if command == "show ip interface Vlan121":
                return {
                    "Vlan121": {
                        "enabled": True,
                        "oper_status": "up",
                        "ipv4": {
                            "192.0.2.10/24": {
                                "ip": "192.0.2.10",
                                "prefix_length": "24",
                                "secondary": False,
                            },
                            "192.0.2.11/24": {
                                "ip": "192.0.2.11",
                                "prefix_length": "24",
                                "secondary": True,
                            },
                        },
                    },
                }
            if command == "show wireless interface summary":
                return {
                    "interfaces": {
                        "Vlan121": {
                            "interface_type": "Management",
                            "vlan_id": 121,
                            "ip_address": "192.0.2.10",
                            "ip_netmask": "255.255.255.0",
                            "nat_ip_address": "0.0.0.0",
                            "mac_address": "001e.496d.ccff",
                        },
                    },
                }
            raise AssertionError(f"Unexpected command: {command}")

        self.device.parse = Mock(side_effect=parse)

        self.stage.verify_wireless_management(
            self.device, _Steps(), max_time=1, check_interval=1
        )

        self.device.parse.assert_has_calls([
            call("show interfaces GigabitEthernet2 trunk"),
            call("show ip interface Vlan121"),
            call("show wireless interface summary"),
        ])

    def test_verify_missing_secondary_ipv4_address_fails(self):
        self.device.management["wireless"].update({
            "switchport": None,
            "address": {
                "ipv4": ["192.0.2.10/24", "192.0.2.11/24"],
            },
        })

        self.device.parse = Mock(return_value={
            "Vlan121": {
                "enabled": True,
                "oper_status": "up",
                "ipv4": {
                    "192.0.2.10/24": {
                        "ip": "192.0.2.10",
                        "prefix_length": "24",
                        "secondary": False,
                    },
                },
            },
        })

        with patch(
                "genie.libs.clean.stages.iosxe.cat9k.c9800.stages.Timeout",
                _OneAttemptTimeout):
            with self.assertRaisesRegex(
                    RuntimeError, "expected IPv4 addresses"):
                self.stage.verify_wireless_management(
                    self.device, _Steps(), max_time=1, check_interval=1
                )

        self.device.parse.assert_called_once_with(
            "show ip interface Vlan121"
        )

    def test_verify_missing_ipv6_address_fails(self):
        self.device.management["wireless"].update({
            "switchport": None,
            "address": {"ipv6": "2001:db8::10/64"},
        })

        def parse(command):
            if command == "show ip interface Vlan121":
                return {
                    "Vlan121": {
                        "enabled": True,
                        "oper_status": "up",
                    },
                }
            if command == "show ipv6 interface brief":
                return {
                    "interface": {
                        "Vlan121": {
                            "interface_state": "up",
                            "protocol_state": "up",
                            "link_local_address": "fe80::1",
                            "ipv6_addresses": ["2001:db8::20"],
                        },
                    },
                }
            raise AssertionError(f"Unexpected command: {command}")

        self.device.parse = Mock(side_effect=parse)
        with patch(
                "genie.libs.clean.stages.iosxe.cat9k.c9800.stages.Timeout",
                _OneAttemptTimeout):
            with self.assertRaisesRegex(
                    RuntimeError, "expected IPv6 addresses"):
                self.stage.verify_wireless_management(
                    self.device, _Steps(), max_time=1, check_interval=1
                )

        self.device.parse.assert_has_calls([
            call("show ip interface Vlan121"),
            call("show ipv6 interface brief"),
        ])

    def test_verify_missing_wireless_summary_interface_fails(self):
        self.device.management["wireless"]["switchport"] = None

        def parse(command):
            if command == "show ip interface Vlan121":
                return {
                    "Vlan121": {
                        "enabled": True,
                        "oper_status": "up",
                        "ipv4": {
                            "192.0.2.10/24": {
                                "ip": "192.0.2.10",
                                "prefix_length": "24",
                                "secondary": False,
                            },
                        },
                    },
                }
            if command == "show wireless interface summary":
                return {}
            raise AssertionError(f"Unexpected command: {command}")

        self.device.parse = Mock(side_effect=parse)

        with self.assertRaisesRegex(
                RuntimeError, "does not show Vlan121 as Management"):
            self.stage.verify_wireless_management(
                self.device, _Steps(), max_time=1, check_interval=1
            )

        self.device.parse.assert_has_calls([
            call("show ip interface Vlan121"),
            call("show wireless interface summary"),
        ])


class TestC9800CLCleanAbstraction(unittest.TestCase):

    def test_inherits_wireless_management_stage(self):
        device = SimpleNamespace(
            os="iosxe",
            platform="cat9k",
            model="c9800",
            submodel="c9800_cl",
        )
        lookup = Lookup.from_device(device, packages={"clean": clean})

        stage = lookup.clean.stages.stages.ConfigureWirelessManagement

        self.assertEqual(
            stage.__module__,
            "genie.libs.clean.stages.iosxe.cat9k.c9800.stages",
        )


if __name__ == "__main__":
    unittest.main()
