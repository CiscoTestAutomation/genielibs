import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    config_port_security_on_interface,
)


class TestConfigPortSecurityOnInterface(TestCase):

    def test_config_port_security_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_port_security_on_interface(
            device,
            "te1/0/1",
            1,
            None,
            None,
            None,
            "70c9.c6b9.abcd",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface te1/0/1", sent_commands)
        self.assertIn("switchport port-security", sent_commands)
        self.assertIn("switchport port-security maximum 1", sent_commands)
        self.assertIn(
            "switchport port-security mac-address 70c9.c6b9.abcd",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()