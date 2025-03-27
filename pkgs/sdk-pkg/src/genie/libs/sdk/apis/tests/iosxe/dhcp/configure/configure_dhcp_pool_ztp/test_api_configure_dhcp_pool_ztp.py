from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_pool_ztp
from unittest.mock import Mock


class TestConfigureDhcpPoolZtp(TestCase):

    def test_configure_dhcp_pool_ztp(self):
        self.device = Mock()
        result = configure_dhcp_pool_ztp(self.device, 'ztp', '10.10.10.0', '255.255.255.0', 67, 'ztp_http_latest.py', 150, '10.10.10.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dhcp pool ztp', 'network 10.10.10.0 255.255.255.0', 'option 67 ascii ztp_http_latest.py', 'option 150 ip 10.10.10.1'],)
        )
