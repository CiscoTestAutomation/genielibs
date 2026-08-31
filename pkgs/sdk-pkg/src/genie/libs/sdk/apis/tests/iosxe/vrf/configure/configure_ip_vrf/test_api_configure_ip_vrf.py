from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_ip_vrf
from unittest.mock import Mock


class TestConfigureIpVrf(TestCase):

    def test_configure_ip_vrf(self):
        self.device = Mock()
        result = configure_ip_vrf(self.device, 'test_vrf', '172.29.66.104:40', 'export', '65002:40')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip vrf test_vrf', 'rd 172.29.66.104:40', 'route-target export 65002:40'],)
        )
