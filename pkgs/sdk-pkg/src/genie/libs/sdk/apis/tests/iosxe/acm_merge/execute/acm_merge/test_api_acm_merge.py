from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm_merge.execute import acm_merge
from unittest.mock import Mock


class TestAcmMerge(TestCase):

    def test_acm_merge(self):
        self.device = Mock()
        results_map = {
            'acm merge flash:checkpoint1': '''Merge the configuration from flash:checkpoint1


            Applying the configlet:flash:checkpoint1
                Apply failed: 
                Failed Command: ^@, error location 0, prc code 0x68, cli line num 0
                Merge Time: 0 msec, Validation Time: 0 msec, Apply Time: 0 msec

            Rollback to snapshot config: flash:snapshot.cfg
                Config diff empty, nothing to validate/replace
                Rollback to snapshot failed''',
                    }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_merge(self.device, 'flash', 'checkpoint1', None, None)
        self.assertIn(
            'acm merge flash:checkpoint1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
