from unittest import TestCase
from genie.libs.sdk.apis.iosxe.segment_routing.configure import unconfigure_segment_routing
from unittest.mock import Mock


class TestUnconfigureSegmentRouting(TestCase):

    def test_unconfigure_segment_routing(self):
        self.device = Mock()
        result = unconfigure_segment_routing(self.device, 'mpls')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no segment-routing mpls',)
        )
