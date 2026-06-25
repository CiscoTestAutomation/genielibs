import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_medium_p2p_interface,
)


class TestConfigureMediumP2pInterface(TestCase):

    def test_configure_medium_p2p_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_medium_p2p_interface(
            device,
            "HundredGigE1/0/49",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface HundredGigE1/0/49", sent_commands)
        self.assertIn("medium p2p", sent_commands)


if __name__ == "__main__":
    unittest.main()