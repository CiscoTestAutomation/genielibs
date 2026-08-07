import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    configure_ipsec_ike_sa_strength_enforcement,
)


class TestConfigureIpsecIkeSaStrengthEnforcement(TestCase):

    def test_configure_ipsec_ike_sa_strength_enforcement(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipsec_ike_sa_strength_enforcement(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            ["crypto ipsec ike sa-strength-enforcement"],
        )


if __name__ == "__main__":
    unittest.main()