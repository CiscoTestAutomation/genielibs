from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_router_bgp_maximum_paths
from unittest.mock import Mock

class TestConfigureRouterBgpMaximumPaths(TestCase):

    def test_configure_router_bgp_maximum_paths(self):
        self.device = Mock()
        configure_router_bgp_maximum_paths(self.device, 65001, 4, None)
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 65001', 'maximum-paths 4'],))
