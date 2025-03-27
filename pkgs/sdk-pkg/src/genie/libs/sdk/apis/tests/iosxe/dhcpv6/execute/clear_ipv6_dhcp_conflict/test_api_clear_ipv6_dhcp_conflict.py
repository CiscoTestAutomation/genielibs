from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.execute import clear_ipv6_dhcp_conflict
from unittest.mock import Mock


class TestClearIpv6DhcpConflict(TestCase):

    def test_clear_ipv6_dhcp_conflict(self):
        self.device = Mock()
        results_map = {
            'clear ipv6 dhcp conflict *': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_ipv6_dhcp_conflict(self.device)
        self.assertIn(
            'clear ipv6 dhcp conflict *',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
