import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    configure_crypto_ikev2_proposal,
)


class TestConfigureCryptoIkev2Proposal(TestCase):

    def test_configure_crypto_ikev2_proposal(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_ikev2_proposal(
            device,
            "pqc-no-optional",
            "aes-cbc-256",
            "sha512 sha384",
            "19 14 21",
            None,
            "mlkem768 mlkem1024",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto ikev2 proposal pqc-no-optional",
                "encryption aes-cbc-256",
                "integrity sha512 sha384",
                "group 19 14 21",
                "pqc mlkem768 mlkem1024",
            ],
        )


if __name__ == "__main__":
    unittest.main()