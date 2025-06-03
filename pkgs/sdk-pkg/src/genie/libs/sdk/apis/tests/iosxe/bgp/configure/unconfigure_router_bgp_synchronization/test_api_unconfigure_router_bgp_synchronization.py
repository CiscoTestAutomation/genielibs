from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_router_bgp_synchronization


class TestUnconfigureRouterBgpSynchronization(TestCase):

    def test_unconfigure_router_bgp_synchronization(self):
        self.device = Mock()
        result = unconfigure_router_bgp_synchronization(self.device, '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 100', 'no synchronization'],)
        )
