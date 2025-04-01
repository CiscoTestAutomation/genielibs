from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ipv6_dhcp_pool
from unittest.mock import Mock


class TestConfigureIpv6DhcpPool(TestCase):

    def test_configure_ipv6_dhcp_pool(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_pool(self.device, 'quakev6', '2001:DB8:10::/64', 'tftp://[2001:db8:10::25]/ztp_http_latest.py')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp pool quakev6', 'address prefix 2001:DB8:10::/64', 'bootfile-url tftp://[2001:db8:10::25]/ztp_http_latest.py'],)
        )
