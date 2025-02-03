from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_ip_host
from unittest.mock import Mock


class TestUnconfigureIpHost(TestCase):

    def test_unconfigure_ip_host(self):
        self.device = Mock()
        result = unconfigure_ip_host(self.device, 'test.com', '1.1.1.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip host test.com 1.1.1.1',)
        )
