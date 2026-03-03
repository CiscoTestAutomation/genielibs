from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ptp.clear import clear_ptp_corrections
from unittest.mock import Mock


class TestClearPtpCorrections(TestCase):

    def test_clear_ptp_corrections(self):
        self.device = Mock()
        results_map = {
            'clear ptp corrections': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_ptp_corrections(self.device)
        self.assertIn(
            'clear ptp corrections',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
