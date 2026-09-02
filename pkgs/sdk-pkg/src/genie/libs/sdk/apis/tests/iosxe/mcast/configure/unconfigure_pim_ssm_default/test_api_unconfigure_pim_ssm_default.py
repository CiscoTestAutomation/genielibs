import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import (
    unconfigure_pim_ssm_default,
)


class TestUnconfigurePimSsmDefault(TestCase):

    def test_unconfigure_pim_ssm_default(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_pim_ssm_default(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no ip pim ssm default",
        )


if __name__ == "__main__":
    unittest.main()
