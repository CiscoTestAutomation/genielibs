import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_sa_global


class TestConfigureIpsecSaGlobal(TestCase):

    def test_configure_ipsec_sa_global(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipsec_sa_global(
            device,
            True,
            False,
            300,
            True,
            False,
            None,
            False,
            False,
            512,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto ipsec security-association ecn discard",
                "crypto ipsec security-association idle-time 300",
                "crypto ipsec security-association lifetime days 1",
                "crypto ipsec security-association replay window-size 512",
                "crypto ipsec security-association multi-sn",
            ],
        )


if __name__ == "__main__":
    unittest.main()