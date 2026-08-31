import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lldp.configure import (
    unconfigure_lldp_holdtime,
)


class TestUnconfigureLldpHoldtime(TestCase):

    def test_unconfigure_lldp_holdtime(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_lldp_holdtime(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no lldp holdtime",
        )


if __name__ == "__main__":
    unittest.main()
