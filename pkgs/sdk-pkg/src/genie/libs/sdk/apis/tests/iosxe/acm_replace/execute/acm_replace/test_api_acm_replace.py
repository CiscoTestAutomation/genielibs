from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm_replace.execute import acm_replace
from unittest.mock import Mock


class TestAcmReplace(TestCase):

    def test_acm_replace(self):
        self.device = Mock()
        results_map = {
            'acm replace flash:checkpoint1': '''Configure Replace to Target config: flash:checkpoint1
    Time taken apply changes = 45 msec (0 sec)
    Config replace success
    Configuration Net-Diff: flash:acm/acm_cfg_REPLACE_diff_3958098268.cfg'''
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_replace(self.device, 'flash', 'checkpoint1', None)
        self.assertIn(
            'acm replace flash:checkpoint1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)