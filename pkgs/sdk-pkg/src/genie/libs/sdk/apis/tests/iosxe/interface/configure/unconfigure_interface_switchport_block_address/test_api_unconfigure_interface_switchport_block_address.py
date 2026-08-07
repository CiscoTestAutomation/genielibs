import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_interface_switchport_block_address,
)


class TestUnconfigureInterfaceSwitchportBlockAddress(TestCase):

    def test_unconfigure_interface_switchport_block_address(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_switchport_block_address(
            device,
            "Tw1/0/4",
            "unicast",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Tw1/0/4",
            sent_commands,
        )
        self.assertIn(
            "no switchport block unicast",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()