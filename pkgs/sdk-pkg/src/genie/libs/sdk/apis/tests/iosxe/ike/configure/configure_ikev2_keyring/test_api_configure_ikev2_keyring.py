import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_keyring


class TestConfigureIkev2Keyring(TestCase):

    def test_configure_ikev2_keyring(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_keyring(
            device,
            "HUB-KEY",
            "1",
            "0.0.0.0",
            "0.0.0.0",
            "cisco",
            False,
            "ppk1",
            "cisco123",
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 keyring HUB-KEY", sent_commands)
        self.assertIn("peer 1", sent_commands)
        self.assertIn("address 0.0.0.0 0.0.0.0", sent_commands)
        self.assertIn("pre-shared-key cisco", sent_commands)
        self.assertIn("ppk manual id ppk1 key cisco123", sent_commands)

    def test_configure_ikev2_keyring_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_keyring(
            device,
            "HUB-KEY",
            "1",
            "0.0.0.0",
            "0.0.0.0",
            "cisco",
            True,
            "ppk2",
            "cisco123",
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 keyring HUB-KEY", sent_commands)
        self.assertIn("peer 1", sent_commands)
        self.assertIn("address 0.0.0.0 0.0.0.0", sent_commands)
        self.assertIn("pre-shared-key cisco", sent_commands)
        self.assertIn("ppk manual id ppk2 key cisco123 required", sent_commands)

    def test_configure_ikev2_keyring_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_keyring(
            device,
            "dynamic",
            "1",
            "0.0.0.0",
            "0.0.0.0",
            "cisco",
            False,
            None,
            None,
            "dynamic1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 keyring dynamic", sent_commands)
        self.assertIn("peer 1", sent_commands)
        self.assertIn("address 0.0.0.0 0.0.0.0", sent_commands)
        self.assertIn("pre-shared-key cisco", sent_commands)
        self.assertIn("ppk dynamic dynamic1", sent_commands)

    def test_configure_ikev2_keyring_3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_keyring(
            device,
            "dynamic",
            "1",
            "0.0.0.0",
            "0.0.0.0",
            None,
            True,
            None,
            None,
            "dynamic1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 keyring dynamic", sent_commands)
        self.assertIn("peer 1", sent_commands)
        self.assertIn("address 0.0.0.0 0.0.0.0", sent_commands)
        self.assertIn("ppk dynamic dynamic1 required", sent_commands)

    def test_configure_ikev2_keyring_4(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_keyring(
            device,
            "manual",
            "1",
            "0.0.0.0",
            "0.0.0.0",
            None,
            False,
            "ppk1",
            "cisco123",
            "dynamic1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("crypto ikev2 keyring manual", sent_commands)
        self.assertIn("peer 1", sent_commands)
        self.assertIn("address 0.0.0.0 0.0.0.0", sent_commands)
        self.assertIn("ppk manual id ppk1 key cisco123", sent_commands)


if __name__ == "__main__":
    unittest.main()