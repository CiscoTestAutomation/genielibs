from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfig_ip_tcp_mss


class TestUnconfigIpTcpMss(TestCase):

    def test_unconfig_ip_tcp_mss(self):
        self.device = Mock()
        unconfig_ip_tcp_mss(self.device, '1500', '1', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip tcp mss 1500' ,)
        )
