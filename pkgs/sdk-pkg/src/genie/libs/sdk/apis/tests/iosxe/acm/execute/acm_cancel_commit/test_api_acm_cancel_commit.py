from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_cancel_commit
from unittest.mock import Mock


class TestAcmCancelCommit(TestCase):

    def test_acm_cancel_commit(self):
        self.device = Mock()
        results_map = {
            'acm cancel-commit': 'Confirm-timer not running.',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_cancel_commit(self.device)
        self.assertIn(
            'acm cancel-commit',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
