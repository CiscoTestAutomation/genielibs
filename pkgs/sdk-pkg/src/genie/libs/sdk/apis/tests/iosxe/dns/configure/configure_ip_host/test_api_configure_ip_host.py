from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_ip_host
from unittest.mock import Mock


class TestConfigureIpHost(TestCase):

    def test_configure_ip_host(self):
        self.device = Mock()
        result = configure_ip_host(self.device, 'test.com', '1.1.1.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip host test.com 1.1.1.1',)
        )
