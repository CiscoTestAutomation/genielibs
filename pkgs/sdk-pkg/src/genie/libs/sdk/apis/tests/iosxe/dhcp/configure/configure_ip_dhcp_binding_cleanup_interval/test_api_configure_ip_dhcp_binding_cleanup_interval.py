from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_binding_cleanup_interval
from unittest.mock import Mock


class TestConfigureIpDhcpBindingCleanupInterval(TestCase):

    def test_configure_ip_dhcp_binding_cleanup_interval(self):
        self.device = Mock()
        result = configure_ip_dhcp_binding_cleanup_interval(self.device, '20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip dhcp binding cleanup interval 20',)
        )
