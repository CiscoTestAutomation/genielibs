from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_router_bgp_synchronization
from unittest.mock import Mock


class TestConfigureRouterBgpSynchronization(TestCase):

    def test_configure_router_bgp_synchronization(self):
        self.device = Mock()
        result = configure_router_bgp_synchronization(self.device, '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 100', 'synchronization'],)
        )
