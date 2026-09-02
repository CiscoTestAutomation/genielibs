from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_private_vlan_on_vlan,
)


class TestConfigurePrivateVlanOnVlan(TestCase):

    def test_configure_private_vlan_on_vlan(self):
        device = Mock()

        result = configure_private_vlan_on_vlan(device, '222', '1222')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vlan 222',
                'private-vlan isolated',
                'vlan 1222',
                'private-vlan primary',
                'private-vlan association 222',
            ]
        )
