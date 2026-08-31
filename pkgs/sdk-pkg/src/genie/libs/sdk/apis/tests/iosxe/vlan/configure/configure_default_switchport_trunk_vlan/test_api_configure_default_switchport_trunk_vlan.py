from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_default_switchport_trunk_vlan,
)


class TestConfigureDefaultSwitchportTrunkVlan(TestCase):

    def test_configure_default_switchport_trunk_vlan(self):
        device = Mock()

        result = configure_default_switchport_trunk_vlan(device, 'Te3/1/8')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface Te3/1/8',
                'default switchport trunk native vlan',
            ]
        )
