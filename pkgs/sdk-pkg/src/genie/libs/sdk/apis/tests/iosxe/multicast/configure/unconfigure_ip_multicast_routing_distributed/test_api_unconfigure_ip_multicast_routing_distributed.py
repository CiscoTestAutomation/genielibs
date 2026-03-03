from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_multicast_routing_distributed

class TestUnconfigureIpMulticastRoutingDistributed(TestCase):

    def test_unconfigure_ip_multicast_routing_distributed(self):
        device = Mock()
        result = unconfigure_ip_multicast_routing_distributed(device, True, 'default')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip multicast-routing distributed no-spd punt-limit default',)
        )