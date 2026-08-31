import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    unconfigure_mka_policy_delay_protection,
)


class TestUnconfigureMkaPolicyDelayProtection(TestCase):

    def test_unconfigure_mka_policy_delay_protection(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mka_policy_delay_protection(
            device,
            "policy1",
            "GigabitEthernet1/0/10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/10",
                "no mka policy policy1",
                "no mka policy policy1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
