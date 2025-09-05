from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import configure_ip_nat_switchover_http
from unittest.mock import Mock


class TestConfigureIpNatSwitchoverHttp(TestCase):

    def test_configure_ip_nat_switchover_http(self):
        self.device = Mock()
        result = configure_ip_nat_switchover_http(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip nat switchover replication http',)
        )