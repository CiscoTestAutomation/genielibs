from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_ip_nat_switchover_http
from unittest.mock import Mock


class TestUnconfigureIpNatSwitchoverHttp(TestCase):

    def test_unconfigure_ip_nat_switchover_http(self):
        self.device = Mock()
        result = unconfigure_ip_nat_switchover_http(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip nat switchover replication http',)
        )