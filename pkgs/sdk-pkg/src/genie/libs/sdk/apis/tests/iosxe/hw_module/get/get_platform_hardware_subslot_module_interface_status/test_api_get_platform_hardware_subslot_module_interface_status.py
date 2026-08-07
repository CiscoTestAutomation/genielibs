import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.hw_module.get import (
    get_platform_hardware_subslot_module_interface_status,
)


class TestGetPlatformHardwareSubslotModuleInterfaceStatus(
        unittest.TestCase):

    def test_get_interface_status(self):
        device = Mock()
        # Parsed 'show platform hardware subslot 0/1 module
        # interface GigabitEthernet0/1/0 status'
        parsed = {
            "l2_network": {
                "link": "down",
                "link_config": "disabled",
                "speed": "unknown",
                "speed_config": "unknown",
                "duplex": "unknown",
                "duplex_config": "unknown",
                "nego_config": "unknown",
                "mtu": 1522,
                "rx_pause": "off",
                "rx_pause_config": "off",
                "tx_pause": "off",
                "tx_pause_config": "off",
            },
            "vlan_mode": "access",
            "native_vlan": 1,
        }
        device.parse = Mock(return_value=parsed)

        result = get_platform_hardware_subslot_module_interface_status(
            device, "0/1", "GigabitEthernet0/1/0")

        device.parse.assert_called_once_with(
            "show platform hardware subslot 0/1 module "
            "interface GigabitEthernet0/1/0 status")
        self.assertEqual(result, parsed)

    def test_get_interface_status_empty(self):
        device = Mock()
        device.parse = Mock(side_effect=SchemaEmptyParserError("empty"))

        result = get_platform_hardware_subslot_module_interface_status(
            device, "0/1", "GigabitEthernet0/1/0")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
