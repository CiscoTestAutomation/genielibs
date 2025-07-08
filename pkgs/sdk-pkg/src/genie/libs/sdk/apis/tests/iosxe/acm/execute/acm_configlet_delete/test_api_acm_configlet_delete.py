from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_configlet_delete
from unittest.mock import Mock


class TestAcmConfigletDelete(TestCase):

    def test_acm_configlet_delete(self):
        self.device = Mock()
        results_map = {
            'acm configlet modify demo delete 1': 'Successfully delete CLI with index : 1',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_configlet_delete(self.device, 'demo', '1')
        self.assertIn(
            'acm configlet modify demo delete 1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
