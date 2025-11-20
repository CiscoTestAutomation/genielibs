from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ipv6_local_pool
from unittest.mock import Mock


class TestConfigureIpv6LocalPool(TestCase):

    def test_configure_ipv6_local_pool(self):
        self.device = Mock()
        result = configure_ipv6_local_pool(self.device, 'IP_POOL_V6', '2001:DB8:0:FFFE::/112', 128)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ipv6 local pool IP_POOL_V6 2001:DB8:0:FFFE::/112 128',)
        )
