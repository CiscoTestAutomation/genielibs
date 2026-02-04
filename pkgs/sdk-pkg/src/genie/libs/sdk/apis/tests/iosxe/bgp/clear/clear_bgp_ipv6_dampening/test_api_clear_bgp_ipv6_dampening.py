from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.clear import clear_bgp_ipv6_dampening
from unittest.mock import Mock


class TestClearBgpIpv6Dampening(TestCase):

    def test_clear_bgp_ipv6_dampening(self):
        self.device = Mock()
        results_map = {
            'clear bgp ipv6 unicast dampening': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_bgp_ipv6_dampening(self.device, None, None)
        self.assertIn(
            'clear bgp ipv6 unicast dampening',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
