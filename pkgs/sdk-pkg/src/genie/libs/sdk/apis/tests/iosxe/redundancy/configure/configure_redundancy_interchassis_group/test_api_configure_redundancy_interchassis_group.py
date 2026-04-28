import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.redundancy.configure import (
    configure_redundancy_interchassis_group,
)


class TestConfigureRedundancyInterchassisGroup(TestCase):

    def test_configure_redundancy_interchassis_group_full(self):
        device = Mock()
        device.state_machine.current_state = 'enable'
        device.name = 'uut'

        result = configure_redundancy_interchassis_group(
            device=device,
            group='4294967295',
            monitor_peer_bfd=True,
            member_ip='88.1.1.2',
            backbone_interface='TenGigabitEthernet0/0/2',
            mlacp_system_mac='0001.0001.0001',
            mlacp_system_priority='100',
            mlacp_node_id='1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'redundancy',
            'interchassis group "4294967295"',
            'monitor peer bfd',
            'member ip "88.1.1.2"',
            'backbone interface "TenGigabitEthernet0/0/2"',
            'mlacp system-mac "0001.0001.0001"',
            'mlacp system-priority "100"',
            'mlacp node-id "1"',
        ])

    def test_configure_redundancy_interchassis_group_required_only(self):
        device = Mock()
        device.state_machine.current_state = 'enable'
        device.name = 'uut'

        result = configure_redundancy_interchassis_group(
            device=device,
            group='4294967295',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'redundancy',
            'interchassis group "4294967295"',
        ])


if __name__ == '__main__':
    unittest.main()
