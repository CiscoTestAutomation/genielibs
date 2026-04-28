import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    unconfigure_ip_igmp_snooping_vlan_static,
)


class TestUnconfigureIpIgmpSnoopingVlanStatic(TestCase):

    def test_unconfigure_ip_igmp_snooping_vlan_static(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_igmp_snooping_vlan_static(
            device,
            "200",
            "225.0.100.100",
            "Te1/0/2",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn(
            "no ip igmp snooping vlan 200 static 225.0.100.100 interface Te1/0/2",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()