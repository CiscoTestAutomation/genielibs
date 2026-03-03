from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_ip_host
from unittest.mock import Mock


class TestConfigureIpHost(TestCase):

    def test_configure_ip_host(self):
        self.device = Mock()
        result = configure_ip_host(self.device, 'host1', ['1.1.1.1', '2.2.2.2', '3.3.3.3'], None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip host host1 1.1.1.1 2.2.2.2 3.3.3.3',)
        )
