import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_sks_client


class TestConfigureSksClient(TestCase):

    def test_configure_sks_client(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_sks_client(
            device,
            "test_block_1",
            "ipv6",
            "9e21:953d:1870:c090:4cf3:51a6:cce8:3337",
            "4321",
            "test_psk_1",
            "test_password_1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto skip-client test_block_1",
                "server ipv6 9e21:953d:1870:c090:4cf3:51a6:cce8:3337 port 4321",
                "psk id test_psk_1 key 0 test_password_1",
            ],
        )

    def test_configure_sks_client_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_sks_client(
            device,
            "test_block_2",
            "ipv4",
            "23.45.21.43",
            "9675",
            "test_psk_2",
            "test_password_2",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto skip-client test_block_2",
                "server ipv4 23.45.21.43 port 9675",
                "psk id test_psk_2 key 0 test_password_2",
            ],
        )


if __name__ == "__main__":
    unittest.main()
