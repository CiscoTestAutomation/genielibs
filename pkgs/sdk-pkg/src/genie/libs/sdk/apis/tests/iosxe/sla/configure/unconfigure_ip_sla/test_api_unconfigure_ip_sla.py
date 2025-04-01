from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sla.configure import unconfigure_ip_sla
from unittest.mock import Mock


class TestUnconfigureIpSla(TestCase):

    def test_unconfigure_ip_sla(self):
        self.device = Mock()
        result = unconfigure_ip_sla(self.device, 2147483647)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip sla 2147483647',)
        )
