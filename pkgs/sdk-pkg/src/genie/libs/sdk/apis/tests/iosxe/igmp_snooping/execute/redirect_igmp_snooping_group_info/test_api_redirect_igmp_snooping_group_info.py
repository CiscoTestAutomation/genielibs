from unittest import TestCase
from genie.libs.sdk.apis.iosxe.igmp_snooping.execute import redirect_igmp_snooping_group_info
from unittest.mock import Mock


class TestRedirectIgmpSnoopingGroupInfo(TestCase):

    def test_redirect_igmp_snooping_group_info(self):
        self.device = Mock()
        results_map = {
            'show tech-support platform igmp-snooping group_ipAddr 239.1.1.1 vlan 10 | redirect bootflash:show_tech_support_igmp_snooping': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = redirect_igmp_snooping_group_info(self.device, 'show_tech_support_igmp_snooping', '239.1.1.1', 10)
        self.assertIn(
            'show tech-support platform igmp-snooping group_ipAddr 239.1.1.1 vlan 10 | redirect bootflash:show_tech_support_igmp_snooping',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
