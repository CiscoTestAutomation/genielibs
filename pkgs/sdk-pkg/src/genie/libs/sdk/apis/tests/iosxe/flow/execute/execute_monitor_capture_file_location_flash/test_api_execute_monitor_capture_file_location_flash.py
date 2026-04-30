from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.execute import execute_monitor_capture_file_location_flash
from unittest.mock import Mock


class TestExecuteMonitorCaptureFileLocationFlash(TestCase):

    def test_execute_monitor_capture_file_location_flash(self):
        self.device = Mock()
        results_map = {
            'monitor capture C3 file location flash:TAC3.pcap interface TwentyFiveGigE1/0/24 in match any':
            'Interface TwentyFiveGigE1/0/24 direction IN is already attached to the capture\n'
            'A filter is already attached to the capture. Replace with specified filter?[confirm]\n'
            'A file name has already been associated, replace?[confirm]\n'
            'A file by the name already exists, overwrite?[confirm]'
}
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_monitor_capture_file_location_flash(self.device, 'C3', 'TAC3.pcap', '', '', 'TwentyFiveGigE1/0/24', 'in', 'any')
        self.assertIn(
            'monitor capture C3 file location flash:TAC3.pcap interface TwentyFiveGigE1/0/24 in match any',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
