from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import unconfigure_ip_host_vrf_view
from unittest.mock import Mock


class TestUnconfigureIpHostVrfView(TestCase):

    def test_unconfigure_ip_host_vrf_view(self):
        self.device = Mock()
        result = unconfigure_ip_host_vrf_view(self.device, 'vrf1', 'view1', 'www.test', '1.1.1.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip host vrf vrf1 view view1 www.test 1.1.1.1',)
        )
