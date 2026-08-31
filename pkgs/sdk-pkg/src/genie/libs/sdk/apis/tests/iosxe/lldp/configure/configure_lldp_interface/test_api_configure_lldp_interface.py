import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lldp.configure import (
    configure_lldp_interface,
)


class TestConfigureLldpInterface(TestCase):

    def test_configure_lldp_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lldp_interface(
            device,
            "Tw1/0/28",
            True,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "lldp run",
                "interface Tw1/0/28",
                "lldp transmit",
                "lldp receive",
            ],
        )


if __name__ == "__main__":
    unittest.main()
