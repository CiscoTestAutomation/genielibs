from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import redistribute_route_metric_vrf_green


class TestRedistributeRouteMetricVrfGreen(TestCase):

    def test_redistribute_route_metric_vrf_green(self):
        device = Mock()
        result = redistribute_route_metric_vrf_green(
            device,
            2,
            'green',
            '65001',
            10
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospf 2 vrf green',
                'redistribute static metric 10',
                'redistribute connected metric 10',
                'redistribute bgp 65001 metric 10'
            ],)
        )