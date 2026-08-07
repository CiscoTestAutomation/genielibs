import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    configure_crypto_ipsec_nat_transparency,
)


class TestConfigureCryptoIpsecNatTransparency(TestCase):

    def test_configure_crypto_ipsec_nat_transparency(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_crypto_ipsec_nat_transparency(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "crypto ipsec nat-transparency udp-encapsulation",
        )


if __name__ == "__main__":
    unittest.main()