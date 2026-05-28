import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_hsrp_interface


class TestConfigureHsrpInterface(TestCase):

    def test_configure_hsrp_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_hsrp_interface(
            device,
            "Te1/0/15",
            "2",
            "10.10.10.11",
            None,
            None,
            None,
            None,
            "0",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Te1/0/15", sent_commands)
        self.assertIn("standby version 2", sent_commands)
        self.assertIn("standby 0  ip 10.10.10.11", sent_commands)


if __name__ == "__main__":
    unittest.main()