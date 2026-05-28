import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    config_link_local_ip_on_interface,
)


class TestConfigLinkLocalIpOnInterface(TestCase):

    def test_config_link_local_ip_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_link_local_ip_on_interface(
            device,
            "vlan101",
            "FE80:10::3",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface vlan101", sent_commands)
        self.assertIn("ipv6 address FE80:10::3 link-local", sent_commands)


if __name__ == "__main__":
    unittest.main()