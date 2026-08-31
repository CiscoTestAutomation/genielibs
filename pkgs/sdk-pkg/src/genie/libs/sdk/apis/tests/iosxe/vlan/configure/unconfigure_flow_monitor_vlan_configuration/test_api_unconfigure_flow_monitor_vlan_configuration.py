import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    unconfigure_flow_monitor_vlan_configuration,
)


class TestUnconfigureFlowMonitorVlanConfiguration(unittest.TestCase):

    def test_unconfigure_flow_monitor_vlan_configuration(self):
        device = Mock()

        result = unconfigure_flow_monitor_vlan_configuration(
            device,
            100,
            'fl_mon_Po',
            's4',
            'input',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vlan configuration 100',
                'no ip flow monitor fl_mon_Po sampler s4 input',
            ]
        )
