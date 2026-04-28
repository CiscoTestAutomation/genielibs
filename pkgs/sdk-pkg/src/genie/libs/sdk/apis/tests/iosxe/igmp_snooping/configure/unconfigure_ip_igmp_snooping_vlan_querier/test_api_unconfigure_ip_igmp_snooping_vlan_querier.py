import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    unconfigure_ip_igmp_snooping_vlan_querier,
)


class TestUnconfigureIpIgmpSnoopingVlanQuerier(TestCase):

    def test_unconfigure_ip_igmp_snooping_vlan_querier(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_igmp_snooping_vlan_querier(
            device,
            100,
            "11.1.1.1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn(
            "no ip igmp snooping vlan 100 querier address 11.1.1.1",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()