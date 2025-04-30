from unittest import TestCase
from genie.libs.sdk.apis.iosxe.matm.execute import show_tech_support_platform_l2_matm
from unittest.mock import Mock


class TestShowTechSupportPlatformL2Matm(TestCase):

    def test_show_tech_support_platform_l2_matm(self):
        self.device = Mock()
        results_map = {
            'show tech-support platform layer2 matm vlan 10 mac 0000.1111.2222 | redirect bootflash:show_tech_support_l2_matm': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_tech_support_platform_l2_matm(self.device, 'show_tech_support_l2_matm', 10, '0000.1111.2222')
        self.assertIn(
            'show tech-support platform layer2 matm vlan 10 mac 0000.1111.2222 | redirect bootflash:show_tech_support_l2_matm',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
