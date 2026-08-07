import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import unconfigure_isis_keychain_key


class TestUnconfigureIsisKeychainKey(TestCase):

    def test_unconfigure_isis_keychain_key(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_isis_keychain_key(device, "testkey")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no key chain testkey",
        )


if __name__ == "__main__":
    unittest.main()
