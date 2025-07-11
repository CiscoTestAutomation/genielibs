from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_configlet_remove
from unittest.mock import Mock


class TestAcmConfigletRemove(TestCase):

    def test_acm_configlet_remove(self):
        self.device = Mock()
        results_map = {
            'acm configlet remove demo': 'Configlet removed and cleaned up',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_configlet_remove(self.device, 'demo')
        self.assertIn(
            'acm configlet remove demo',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
