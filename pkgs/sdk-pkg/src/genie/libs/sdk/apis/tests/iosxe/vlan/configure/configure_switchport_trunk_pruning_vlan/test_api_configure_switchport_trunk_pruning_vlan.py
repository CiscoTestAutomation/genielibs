import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_switchport_trunk_pruning_vlan,
)


class TestConfigureSwitchportTrunkPruningVlan(unittest.TestCase):

    def test_configure_switchport_trunk_pruning_vlan(self):
        device = Mock()

        result = configure_switchport_trunk_pruning_vlan(
            device,
            'HundredGigE1/0/5',
            '3',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface HundredGigE1/0/5',
                'switchport trunk pruning vlan 3',
            ]
        )
