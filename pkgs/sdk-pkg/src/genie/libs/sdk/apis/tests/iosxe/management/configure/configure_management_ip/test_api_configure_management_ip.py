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


if __name__ == "__main__":
    unittest.main()
