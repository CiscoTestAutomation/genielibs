import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lldp.configure import clear_lldp_counters


class TestClearLldpCounters(TestCase):

    def test_clear_lldp_counters(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = clear_lldp_counters(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "clear lldp counters",
        )


if __name__ == "__main__":
    unittest.main()
