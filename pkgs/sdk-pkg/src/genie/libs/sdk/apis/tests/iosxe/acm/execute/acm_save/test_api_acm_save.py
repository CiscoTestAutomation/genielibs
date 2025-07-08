from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acm.execute import acm_save
from unittest.mock import Mock


class TestAcmSave(TestCase):

    def test_acm_save(self):
        self.device = Mock()
        results_map = {
            'acm save flash:checkpoint1': '''There is a file already existing with this name
        Warning:Do you wish to overwrite the Checkpoint[confirm]
        Successfully created checkpoint flash:/checkpoint1
        sda-9k-5#
        sda-9k-5#
        sda-9k-5#
        sda-9k-5#''',
                }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = acm_save(self.device, 'flash:', 'checkpoint1', None, 60)
        self.assertIn(
            'acm save flash:checkpoint1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
