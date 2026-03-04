from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_ip_dns_view
from unittest.mock import Mock


class TestUnconfigureIpDnsView(TestCase):

    def test_unconfigure_ip_dns_view(self):
        self.device = Mock()
        result = unconfigure_ip_dns_view(self.device, 'view11', False, 'vrf1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dns view vrf vrf1 view11',)
        )
