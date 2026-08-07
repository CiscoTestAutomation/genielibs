import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_mdns_on_interface_vlan,
)


class TestUnconfigureMdnsOnInterfaceVlan(TestCase):

    def test_unconfigure_mdns_on_interface_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mdns_on_interface_vlan(
            device,
            55,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface vlan 55",
            sent_commands,
        )
        self.assertIn(
            "no mdns-sd gateway",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()