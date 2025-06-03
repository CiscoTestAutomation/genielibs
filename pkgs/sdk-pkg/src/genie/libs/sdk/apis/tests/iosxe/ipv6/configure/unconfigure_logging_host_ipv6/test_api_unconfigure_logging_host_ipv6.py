from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import unconfigure_logging_host_ipv6
from unittest.mock import Mock


class TestUnconfigureLoggingHostIpv6(TestCase):

    def test_unconfigure_logging_host_ipv6(self):
        self.device = Mock()
        result = unconfigure_logging_host_ipv6(self.device, '2001:db8::1', 'udp', '2001:db8::1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no logging host ipv6 2001:db8::1 transport udp'],)
        )
