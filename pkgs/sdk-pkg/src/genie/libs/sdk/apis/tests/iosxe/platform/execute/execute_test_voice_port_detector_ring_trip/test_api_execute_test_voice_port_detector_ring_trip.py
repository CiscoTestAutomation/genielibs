from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_test_voice_port_detector_ring_trip
from unittest.mock import Mock


class TestExecuteTestVoicePortDetectorRingTrip(TestCase):

    def test_execute_test_voice_port_detector_ring_trip(self):
        self.device = Mock()
        results_map = {
            'test voice port 1/0/0 detector ring-trip off': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_voice_port_detector_ring_trip(self.device, '1/0/0', 'off')
        self.assertIn(
            'test voice port 1/0/0 detector ring-trip off',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
