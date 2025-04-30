from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mld_snooping.get import show_tech_support_platform_mld_snooping
from unittest.mock import Mock


class TestShowTechSupportPlatformMldSnooping(TestCase):

    def test_show_tech_support_platform_mld_snooping(self):
        self.device = Mock()
        results_map = {
            'show tech-support platform mld_snooping Group_ipv6Addr ff05::1 vlan 10 | redirect bootflash:show_tech_support_mld_snooping': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_tech_support_platform_mld_snooping(self.device, 'show_tech_support_mld_snooping', 'ff05::1', 10)
        self.assertIn(
            'show tech-support platform mld_snooping Group_ipv6Addr ff05::1 vlan 10 | redirect bootflash:show_tech_support_mld_snooping',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
