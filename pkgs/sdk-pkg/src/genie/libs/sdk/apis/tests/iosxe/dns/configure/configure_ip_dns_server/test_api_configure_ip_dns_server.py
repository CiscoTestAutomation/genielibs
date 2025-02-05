from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_ip_dns_server
from unittest.mock import Mock


class TestConfigureIpDnsServer(TestCase):

    def test_configure_ip_dns_server(self):
        self.device = Mock()
        result = configure_ip_dns_server(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip dns server',)
        )
