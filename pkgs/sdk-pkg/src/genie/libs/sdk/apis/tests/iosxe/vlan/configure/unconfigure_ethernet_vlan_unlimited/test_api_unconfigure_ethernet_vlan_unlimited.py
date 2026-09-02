import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import (
    unconfigure_ethernet_vlan_unlimited,
)


class TestUnconfigureEthernetVlanUnlimited(unittest.TestCase):

    def test_unconfigure_ethernet_vlan_unlimited(self):
        device = Mock()

        result = unconfigure_ethernet_vlan_unlimited(device, '0/0')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no hw-module subslot 0/0 ethernet vlan unlimited'
        )
