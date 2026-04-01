from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import redistribute_bgp_metric_route_map_under_ospf


class TestRedistributeBgpMetricRouteMapUnderOspf(TestCase):

    def test_redistribute_bgp_metric_route_map_under_ospf(self):
        device = Mock()
        result = redistribute_bgp_metric_route_map_under_ospf(
            device,
            1,
            1,
            100,
            'ospf_test'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'redistribute bgp 1 metric 100 route-map ospf_test'],)
        )