from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_rollback
from unittest.mock import Mock


class TestAcmRollback(TestCase):

    def test_acm_rollback(self):
        self.device = Mock()
        results_map = {
                'acm rollback 0': '''Configure Rollback to Target config: flash:/checkpoint1
        Config diff empty, nothing to validate/replace''',
            }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_rollback(self.device, '0', 60, None)
        self.assertIn(
            'acm rollback 0',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
