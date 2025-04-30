from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.get import show_tech_support_l3_mroute
from unittest.mock import Mock


class TestShowTechSupportL3Mroute(TestCase):

    def test_show_tech_support_l3_mroute(self):
        self.device = Mock()
        results_map = {
            'show tech-support platform layer3 multicast vrf red group_ipv6Addr ff05::1 srcv6Ip 2001:db8:0:1::1 | redirect bootflash:show_tech_support_l3_mroute': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_tech_support_l3_mroute(self.device, 'show_tech_support_l3_mroute', None, None, 'ff05::1', '2001:db8:0:1::1', 'red')
        self.assertIn(
            'show tech-support platform layer3 multicast vrf red group_ipv6Addr ff05::1 srcv6Ip 2001:db8:0:1::1 | redirect bootflash:show_tech_support_l3_mroute',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
