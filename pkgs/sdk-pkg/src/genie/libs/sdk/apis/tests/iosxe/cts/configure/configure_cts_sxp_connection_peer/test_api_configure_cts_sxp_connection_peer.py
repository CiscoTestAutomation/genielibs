from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_cts_sxp_connection_peer
from unittest.mock import Mock


class TestConfigureCtsSxpConnectionPeer(TestCase):

    def test_configure_cts_sxp_connection_peer(self):
        self.device = Mock()
        result = configure_cts_sxp_connection_peer(self.device, '1100:1:1::1', '1100:1:1::2', 'default', 'local', 'listener', None, True, 90, 180)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts sxp connection peer 1100:1:1::1 source 1100:1:1::2 password default mode local listener hold-time 90 180'],)
        )
