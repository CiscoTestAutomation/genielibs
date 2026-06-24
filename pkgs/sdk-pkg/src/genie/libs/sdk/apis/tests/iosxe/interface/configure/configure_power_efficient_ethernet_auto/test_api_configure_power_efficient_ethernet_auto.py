import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_power_efficient_ethernet_auto,
)


class TestConfigurePowerEfficientEthernetAuto(TestCase):

    def test_configure_power_efficient_ethernet_auto(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_power_efficient_ethernet_auto(
            device,
            "te1/0/5",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface te1/0/5", sent_commands)
        self.assertIn("power efficient-ethernet auto", sent_commands)


if __name__ == "__main__":
    unittest.main()