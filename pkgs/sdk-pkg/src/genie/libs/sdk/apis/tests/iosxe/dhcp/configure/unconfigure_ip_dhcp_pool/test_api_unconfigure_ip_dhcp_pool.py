from unittest import TestCase
from unittest.mock import Mock
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_pool


class TestUnconfigureIpDhcpPool(TestCase):
    def test_unconfigure_ip_dhcp_pool(self):
        self.device = Mock()
        unconfigure_ip_dhcp_pool(self.device, ' POOL_88')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dhcp pool  POOL_88',))
