from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    configure_ethernet_vlan_unlimited,
)


class TestConfigureEthernetVlanUnlimited(TestCase):

    def test_configure_ethernet_vlan_unlimited(self):
        device = Mock()

        result = configure_ethernet_vlan_unlimited(device, '0/0')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'hw-module subslot 0/0 ethernet vlan unlimited'
        )
