from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dns.configure import configure_ip_host_vrf_view
from unittest.mock import Mock


class TestConfigureIpHostVrfView(TestCase):

    def test_configure_ip_host_vrf_view(self):
        self.device = Mock()
        result = configure_ip_host_vrf_view(self.device, 'vrf1', 'view1', 'www.test', '1.1.1.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip host vrf vrf1 view view1 www.test 1.1.1.1',)
        )
