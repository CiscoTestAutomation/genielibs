from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_platform_ip_multicast_ssdp
from unittest.mock import Mock


class TestUnconfigurePlatformIpMulticastSsdp(TestCase):

    def test_unconfigure_platform_ip_multicast_ssdp(self):
        self.device = Mock()
        result = unconfigure_platform_ip_multicast_ssdp(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no platform ip multicast ssdp',)
        )
