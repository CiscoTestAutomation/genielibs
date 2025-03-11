from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_binding_cleanup_interval
from unittest.mock import Mock


class TestUnconfigureIpDhcpBindingCleanupInterval(TestCase):

    def test_unconfigure_ip_dhcp_binding_cleanup_interval(self):
        self.device = Mock()
        result = unconfigure_ip_dhcp_binding_cleanup_interval(self.device, '20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dhcp binding cleanup interval 20',)
        )
