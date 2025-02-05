from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_ip_dns_server
from unittest.mock import Mock


class TestUnconfigureIpDnsServer(TestCase):

    def test_unconfigure_ip_dns_server(self):
        self.device = Mock()
        result = unconfigure_ip_dns_server(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dns server',)
        )
