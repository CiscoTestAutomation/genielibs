from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_platform_ip_multicast_ssdp
from unittest.mock import Mock


class TestConfigurePlatformIpMulticastSsdp(TestCase):

    def test_configure_platform_ip_multicast_ssdp(self):
        self.device = Mock()
        result = configure_platform_ip_multicast_ssdp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('platform ip multicast ssdp',)
        )
