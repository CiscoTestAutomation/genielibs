import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_power_efficient_ethernet_auto,
)


class TestUnconfigurePowerEfficientEthernetAuto(TestCase):

    def test_unconfigure_power_efficient_ethernet_auto(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_power_efficient_ethernet_auto(
            device,
            "te1/0/1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface te1/0/1",
            sent_commands,
        )
        self.assertIn(
            "no power efficient-ethernet auto",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()