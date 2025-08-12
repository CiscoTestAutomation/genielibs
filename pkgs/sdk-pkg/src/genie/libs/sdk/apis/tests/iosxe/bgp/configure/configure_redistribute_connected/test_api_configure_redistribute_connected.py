from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_redistribute_connected
from unittest.mock import Mock

class TestConfigureRedistributeConnected(TestCase):

    def test_configure_redistribute_connected(self):
        self.device = Mock()
        configure_redistribute_connected(self.device, 1, 'ipv4', None, 'rm-adv-loopback')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 1','address-family ipv4','redistribute connected route-map rm-adv-loopback'],))
