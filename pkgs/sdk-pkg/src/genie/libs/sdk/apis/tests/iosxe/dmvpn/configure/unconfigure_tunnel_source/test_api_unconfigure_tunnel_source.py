from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_tunnel_source
from unittest.mock import Mock

class TestUnconfigureTunnelSource(TestCase):

    def test_unconfigure_tunnel_source(self):
        self.device = Mock()
        unconfigure_tunnel_source(self.device, 'gig1', 'tu0')
        self.device.configure.assert_called_with(['interface tu0', 'no tunnel source gig1'])
        
