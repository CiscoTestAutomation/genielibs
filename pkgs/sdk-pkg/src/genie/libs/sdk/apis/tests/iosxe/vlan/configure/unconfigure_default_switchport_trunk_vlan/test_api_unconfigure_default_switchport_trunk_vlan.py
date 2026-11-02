from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    unconfigure_default_switchport_trunk_vlan,
)


class TestUnconfigureDefaultSwitchportTrunkVlan(TestCase):

    def test_unconfigure_default_switchport_trunk_vlan(self):
        device = Mock()
        result = unconfigure_default_switchport_trunk_vlan(
            device,
            'Te3/1/8',
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface Te3/1/8',
            'default switchport trunk native vlan',
        ])
