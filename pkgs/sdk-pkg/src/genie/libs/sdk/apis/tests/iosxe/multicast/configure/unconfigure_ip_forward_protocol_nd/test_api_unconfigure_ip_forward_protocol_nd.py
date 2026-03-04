from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_forward_protocol_nd

class TestUnconfigureIpForwardProtocolNd(TestCase):

    def test_unconfigure_ip_forward_protocol_nd(self):
        device = Mock()
        result = unconfigure_ip_forward_protocol_nd(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip forward-protocol nd',)
        )