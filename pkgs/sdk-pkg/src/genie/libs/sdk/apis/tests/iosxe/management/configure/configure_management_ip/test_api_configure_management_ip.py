import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_ip,
)


class TestConfigureManagementIp(TestCase):

    def test_configure_management_ip(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        device.management = {
            "interface": "GigabitEthernet0",
            "vrf": "Mgmt-intf",
            "address": {
                "ipv4": "10.29.30.167/32",
            },
        }

        result = configure_management_ip(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0",
                "vrf forwarding Mgmt-intf",
                "ip address 10.29.30.167 255.255.255.255",
                "no shutdown",
            ],
        )

    def test_disable_management_vrf_fallback(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.management = {
            "interface": "GigabitEthernet0",
            "vrf": "Mgmt-vrf",
        }

        configure_management_ip(
            device,
            interface="Vlan121",
            address={"ipv4": "192.0.2.10/24"},
            fallback_to_management_vrf=False,
        )

        device.api.configure_management_vrf.assert_not_called()
        device.configure.assert_called_once_with([
            "interface Vlan121",
            "ip address 192.0.2.10 255.255.255.0",
            "no shutdown",
        ])


if __name__ == "__main__":
    unittest.main()
