from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_access_vlan,
)


class TestConfigureAccessVlan(TestCase):

    def test_configure_access_vlan(self):
        device = Mock()

        result = configure_access_vlan(
            device=device,
            vlanid=100,
            interface='GigabitEthernet3/0/1',
        )

        self.assertTrue(result)
        device.configure.assert_called_once_with(
            [
                'int GigabitEthernet3/0/1',
                'switchport mode access',
                'switchport access vlan 100',
                'no shutdown',
            ]
        )
