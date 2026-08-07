import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.ios.interface.configure import (
    unconfigure_pppoe_enable_interface,
)


class TestUnconfigurePppoeEnableInterface(TestCase):

    def test_unconfigure_pppoe_enable_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_pppoe_enable_interface(
            device,
            "Ethernet0/2/0",
            "global",
            "100",
            "1590",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Ethernet0/2/0", sent_commands)
        self.assertIn("no pppoe enable group global", sent_commands)
        self.assertIn("no pppoe-client dial-pool-number 100", sent_commands)
        self.assertIn("no pppoe-client ppp-max-payload 1590", sent_commands)
