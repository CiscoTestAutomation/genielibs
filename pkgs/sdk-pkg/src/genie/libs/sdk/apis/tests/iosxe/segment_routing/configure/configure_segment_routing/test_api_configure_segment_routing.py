from unittest import TestCase
from genie.libs.sdk.apis.iosxe.segment_routing.configure import configure_segment_routing
from unittest.mock import Mock


class TestConfigureSegmentRouting(TestCase):

    def test_configure_segment_routing(self):
        self.device = Mock()
        result = configure_segment_routing(self.device, 'mpls', '800000', '840000', 'ipv4', '98.0.0.1', '32', '4505', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['segment-routing mpls', 'global-block 800000 840000', 'connected-prefix-sid-map', 'address-family ipv4', '98.0.0.1/32 index 4505 range 1'],)
        )
