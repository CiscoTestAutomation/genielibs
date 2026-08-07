import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_keychain_key


class TestConfigureIsisKeychainKey(TestCase):

    def test_configure_isis_keychain_key(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_isis_keychain_key(
            device,
            "testkey",
            "1",
            "testpwd",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "key  chain testkey",
                "key 1",
                "key-string testpwd",
            ],
        )


if __name__ == "__main__":
    unittest.main()