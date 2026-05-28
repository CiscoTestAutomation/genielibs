import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import config_ip_on_interface


class TestConfigIpOnInterface(TestCase):

    def test_config_ip_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = ""

        result = config_ip_on_interface(
            device,
            "g1/0/1",
            None,
            None,
            None,
            None,
            None,
            None,
            False,
            False,
            "",
            None,
            None,
            False,
            "poo1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("interface g1/0/1", sent_commands)
        self.assertIn("ipv6 dhcp client pd poo1", sent_commands)


if __name__ == "__main__":
    unittest.main()