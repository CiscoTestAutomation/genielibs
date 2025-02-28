from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_svi_vlan_range
from unittest.mock import Mock


class TestUnconfigSviVlanRange(TestCase):

    def test_unconfig_svi_vlan_range(self):
        self.device = Mock()
        result = unconfig_svi_vlan_range(self.device, '100', '102', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no interface range vlan 100-102',)
        )
