import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    unconfigure_igmp_snooping_tcn_flood,
)


class TestUnconfigureIgmpSnoopingTcnFlood(TestCase):

    def test_unconfigure_igmp_snooping_tcn_flood(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_igmp_snooping_tcn_flood(
            device,
            "GigabitEthernet2/0/1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet2/0/1", sent_commands)
        self.assertIn("no ip igmp snooping tcn flood", sent_commands)


if __name__ == "__main__":
    unittest.main()