from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_pool_functions
from unittest.mock import Mock


class TestConfigureIpv6DhcpPoolFunctions(TestCase):

    def test_configure_ipv6_dhcp_pool_functions(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_pool_functions(self.device, 'POOL_88', 'vendor-specific', None, None, None, None, None, '17', 'suboption', '13', 'cisco')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp pool POOL_88', 'vendor-specific 17', 'suboption 13 ascii cisco'],)
        )
