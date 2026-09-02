import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    configure_mka_policy,
)


class TestConfigureMkaPolicy(TestCase):

    def test_configure_mka_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_mka_policy(
            device,
            "policy1",
            "GigabitEthernet1/0/10",
            "gcm-aes-256",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "mka policy policy1",
                "macsec-cipher-suite gcm-aes-256",
                "interface GigabitEthernet1/0/10",
                "mka policy policy1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
