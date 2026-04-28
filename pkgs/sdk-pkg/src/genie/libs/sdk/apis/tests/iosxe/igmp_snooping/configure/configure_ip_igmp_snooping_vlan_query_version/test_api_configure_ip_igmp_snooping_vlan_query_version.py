import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    configure_ip_igmp_snooping_vlan_query_version,
)


class TestConfigureIpIgmpSnoopingVlanQueryVersion(TestCase):

    def test_configure_ip_igmp_snooping_vlan_query_version(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_vlan_query_version(
            device,
            100,
            2,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn(
            "ip igmp snooping vlan 100 querier version 2",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()