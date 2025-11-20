from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_ipv6_local_pool
from unittest.mock import Mock


class TestUnconfigureIpv6LocalPool(TestCase):

    def test_unconfigure_ipv6_local_pool(self):
        self.device = Mock()
        result = unconfigure_ipv6_local_pool(self.device, 'IP_POOL_V6')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ipv6 local pool IP_POOL_V6',)
        )
