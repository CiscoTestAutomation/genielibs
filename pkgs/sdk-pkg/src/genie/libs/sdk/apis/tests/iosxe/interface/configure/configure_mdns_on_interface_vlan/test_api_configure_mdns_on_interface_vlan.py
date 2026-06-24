import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_mdns_on_interface_vlan,
)


class TestConfigureMdnsOnInterfaceVlan(TestCase):

    def test_configure_mdns_on_interface_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_mdns_on_interface_vlan(
            device,
            55,
            "policy1",
            60,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface vlan 55", sent_commands)
        self.assertIn("mdns-sd gateway", sent_commands)
        self.assertIn("service-policy policy1", sent_commands)
        self.assertIn("active-query timer 60", sent_commands)


if __name__ == "__main__":
    unittest.main()