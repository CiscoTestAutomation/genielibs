from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_msdp_vrf_peer

class TestUnconfigureIpMsdpVrfPeer(TestCase):

    def test_unconfigure_ip_msdp_vrf_peer(self):
        device = Mock()
        result = unconfigure_ip_msdp_vrf_peer(device, '6.6.6.1', 'red', 'loopback1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip msdp vrf red peer 6.6.6.1 connect-source loopback1',)
        )