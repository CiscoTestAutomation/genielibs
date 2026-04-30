import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    configure_igmp_snooping_tcn_flood,
)


class TestConfigureIgmpSnoopingTcnFlood(TestCase):

    def test_configure_igmp_snooping_tcn_flood(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_igmp_snooping_tcn_flood(
            device,
            "GigabitEthernet2/0/1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet2/0/1", sent_commands)
        self.assertIn("ip igmp snooping tcn flood", sent_commands)


if __name__ == "__main__":
    unittest.main()