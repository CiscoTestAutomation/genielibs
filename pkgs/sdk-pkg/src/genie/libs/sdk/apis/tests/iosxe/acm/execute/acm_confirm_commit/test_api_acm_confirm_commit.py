from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_confirm_commit
from unittest.mock import Mock


class TestAcmConfirmCommit(TestCase):

    def test_acm_confirm_commit(self):
        self.device = Mock()
        results_map = {
            'acm confirm-commit': 'Confirm timer not running',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_confirm_commit(self.device)
        self.assertIn(
            'acm confirm-commit',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
