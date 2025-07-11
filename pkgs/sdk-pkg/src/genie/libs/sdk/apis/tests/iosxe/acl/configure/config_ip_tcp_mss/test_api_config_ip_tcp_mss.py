from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import config_ip_tcp_mss
from unittest.mock import Mock

class TestConfigIpTcpMss(TestCase):

    def test_config_ip_tcp_mss(self):
        self.device = Mock()
        config_ip_tcp_mss(self.device, '1500', '1', None)
        self.device.configure.assert_called_with('ip tcp mss 1500')
