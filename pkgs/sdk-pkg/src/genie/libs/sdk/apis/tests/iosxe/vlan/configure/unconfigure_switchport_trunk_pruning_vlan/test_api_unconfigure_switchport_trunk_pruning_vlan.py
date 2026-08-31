import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    unconfigure_switchport_trunk_pruning_vlan,
)


class TestUnconfigureSwitchportTrunkPruningVlan(unittest.TestCase):

    def test_unconfigure_switchport_trunk_pruning_vlan(self):
        device = Mock()

        result = unconfigure_switchport_trunk_pruning_vlan(
            device,
            'HundredGigE1/0/5',
            '3',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface HundredGigE1/0/5',
                'no switchport trunk pruning vlan 3',
            ]
        )
