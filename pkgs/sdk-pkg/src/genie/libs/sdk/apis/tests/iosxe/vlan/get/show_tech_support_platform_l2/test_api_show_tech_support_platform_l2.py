from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vlan.get import show_tech_support_platform_l2
from unittest.mock import Mock


class TestShowTechSupportPlatformL2(TestCase):

    def test_show_tech_support_platform_l2(self):
        self.device = Mock()
        results_map = {
            'show tech-support platform layer2 vp interface FiftyGigE10/0/1 vlan 10 | redirect bootflash:show_tech_support_l2': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_tech_support_platform_l2(self.device, 'show_tech_support_l2', 10, 'FiftyGigE10/0/1', None)
        self.assertIn(
            'show tech-support platform layer2 vp interface FiftyGigE10/0/1 vlan 10 | redirect bootflash:show_tech_support_l2',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
