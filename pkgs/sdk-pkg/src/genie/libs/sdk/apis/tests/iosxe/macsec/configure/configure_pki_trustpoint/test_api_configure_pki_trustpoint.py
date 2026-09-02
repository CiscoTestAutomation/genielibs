import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    configure_pki_trustpoint,
)


class TestConfigurePkiTrustpoint(TestCase):

    def test_configure_pki_trustpoint(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_pki_trustpoint(
            device,
            None,
            "client",
            None,
            "terminal",
            None,
            "none",
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto pki trustpoint client",
                "enrollment terminal",
                "revocation-check none",
            ],
        )


if __name__ == "__main__":
    unittest.main()
