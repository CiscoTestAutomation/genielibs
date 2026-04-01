from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.clear import clear_bgp_ipv6_neighbor_soft
from unittest.mock import Mock


class TestClearBgpIpv6NeighborSoft(TestCase):

    def test_clear_bgp_ipv6_neighbor_soft(self):
        self.device = Mock()
        results_map = {
            'clear bgp ipv6 unicast 20::2 soft out': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_bgp_ipv6_neighbor_soft(self.device, '20::2', 'out')
        self.assertIn(
            'clear bgp ipv6 unicast 20::2 soft out',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
