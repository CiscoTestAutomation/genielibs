from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.clear import clear_platform_software_fed_matm_stats
from unittest.mock import Mock


class TestClearPlatformSoftwareFedMatmStats(TestCase):

    def test_clear_platform_software_fed_matm_stats(self):
        self.device = Mock()
        results_map = {
            'clear platform software fed switch active matm stats': 'Stats cleared.',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_platform_software_fed_matm_stats(self.device, 'active')
        self.assertIn(
            'clear platform software fed switch active matm stats',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
