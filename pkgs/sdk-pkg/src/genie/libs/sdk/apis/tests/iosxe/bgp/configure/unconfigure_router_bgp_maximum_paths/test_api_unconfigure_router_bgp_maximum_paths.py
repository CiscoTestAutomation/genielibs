
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_router_bgp_maximum_paths


class TestUnconfigureRouterBgpMaximumPaths(TestCase):

    def test_unconfigure_router_bgp_maximum_paths(self):
        self.device = Mock()
        result = unconfigure_router_bgp_maximum_paths(self.device, '100', '3')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 100', 'no maximum-paths 3'],)
        )
