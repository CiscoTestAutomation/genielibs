from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_confederation_peers
from unittest.mock import Mock


class TestConfigureBgpConfederationPeers(TestCase):

    def test_configure_bgp_confederation_peers(self):
        self.device = Mock()
        result = configure_bgp_confederation_peers(self.device, 50, ['200', '300'])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 50', 'bgp confederation peers 200 300', 'exit'],)
        )
