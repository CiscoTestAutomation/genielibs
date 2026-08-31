import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    configure_mac_address_change_interval,
)


class TestConfigureMacAddressChangeInterval(TestCase):

    def test_configure_mac_address_change_interval(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_mac_address_change_interval(
            device,
            10,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "mac-address notification change interval 10",
            ],
        )


if __name__ == "__main__":
    unittest.main()
