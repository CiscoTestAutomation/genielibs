from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_ip_dns_view
from unittest.mock import Mock


class TestConfigureIpDnsView(TestCase):

    def test_configure_ip_dns_view(self):
        self.device = Mock()
        result = configure_ip_dns_view(self.device, 'True', None, None, False, 'forwarding')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip dns view default\nno dns forwarding',)
        )
