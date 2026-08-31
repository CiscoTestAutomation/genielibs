import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    configure_mka_macsec,
)


class TestConfigureMkaMacsec(TestCase):

    def test_configure_mka_macsec(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_mka_macsec(
            device,
            "Te0/1/1",
            "K1",
            "POLICY",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Te0/1/1",
                "mka pre-shared-key key-chain K1",
                "mka policy POLICY",
                "macsec",
            ],
        )


if __name__ == "__main__":
    unittest.main()
