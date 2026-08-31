import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    unconfig_macsec_should_secure,
)


class TestUnconfigMacsecShouldSecure(TestCase):

    def test_unconfig_macsec_should_secure(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_macsec_should_secure(
            device=device,
            interface="TwentyFiveGigE 1/0/7",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE 1/0/7",
                "no macsec access-control should-secure",
            ],
        )


if __name__ == "__main__":
    unittest.main()
