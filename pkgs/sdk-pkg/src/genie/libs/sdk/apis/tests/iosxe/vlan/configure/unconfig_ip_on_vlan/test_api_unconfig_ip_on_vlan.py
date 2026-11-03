from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfig_ip_on_vlan


class TestUnconfigIpOnVlan(TestCase):

    def test_unconfig_ip_on_vlan(self):
        device = Mock()
        result = unconfig_ip_on_vlan(
            device,
            '101',
            '10.230.62.50',
            '255.255.255.0',
            secondary=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with([
            'interface vlan 101',
            'no ip address 10.230.62.50 255.255.255.0 secondary',
        ])
