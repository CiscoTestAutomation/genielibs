import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_isakmp_key


class TestConfigureIsakmpKey(TestCase):

    def test_configure_isakmp_key(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isakmp_key(
            device,
            "test123",
            "0",
            None,
            None,
            None,
            "2007:1::44/112",
            "True",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "crypto isakmp key 0 test123 address ipv6 2007:1::44/112 no-xauth",
            sent_commands,
        )

    def test_configure_isakmp_key_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isakmp_key(
            device,
            "ash123",
            "0",
            "20.18.19.5",
            "255.255.255.0",
            None,
            None,
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "crypto isakmp key 0 ash123 address 20.18.19.5 255.255.255.0",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()