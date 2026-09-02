import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_switchport_trunk_pruning_vlan_except,
)


class TestConfigureSwitchportTrunkPruningVlanExcept(unittest.TestCase):

    def test_configure_switchport_trunk_pruning_vlan_except(self):
        device = Mock()

        result = configure_switchport_trunk_pruning_vlan_except(
            device,
            'Gi1/0/7',
            '1',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Gi1/0/7',
                'switchport trunk pruning vlan except 1',
            ]
        )
