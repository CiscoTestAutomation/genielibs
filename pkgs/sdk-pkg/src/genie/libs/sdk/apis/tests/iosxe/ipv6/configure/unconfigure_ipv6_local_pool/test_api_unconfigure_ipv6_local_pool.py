from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipv6.configure import unconfigure_ipv6_local_pool
from unittest.mock import Mock


class TestUnconfigureIpv6LocalPool(TestCase):

    def test_unconfigure_ipv6_local_pool(self):
        self.device = Mock()
        result = unconfigure_ipv6_local_pool(self.device, 'ipv6_local_pool')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 local pool ipv6_local_pool'],)
        )
