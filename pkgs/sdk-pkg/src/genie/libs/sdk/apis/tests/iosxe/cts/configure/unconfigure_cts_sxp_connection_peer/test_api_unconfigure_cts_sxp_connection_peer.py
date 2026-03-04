from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import unconfigure_cts_sxp_connection_peer
from unittest.mock import Mock


class TestUnconfigureCtsSxpConnectionPeer(TestCase):

    def test_unconfigure_cts_sxp_connection_peer(self):
        self.device = Mock()
        result = unconfigure_cts_sxp_connection_peer(self.device, '1.1.1.1', '2.2.2.2', 'default', 'local', 'listener', None, True, 10, 20)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no cts sxp connection peer 1.1.1.1 source 2.2.2.2 password default mode local listener hold-time 10 20'],)
        )
