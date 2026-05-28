import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_auth_vlan_no_resp,
)


class TestConfigureInterfaceAuthVlanNoResp(TestCase):

    def test_configure_interface_auth_vlan_no_resp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_auth_vlan_no_resp(
            device,
            "GigabitEthernet1/0/3",
            100,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/3", sent_commands)
        self.assertIn(
            "authentication event no-response action authorize vlan 100",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()