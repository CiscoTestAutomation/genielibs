from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_monitor_capture
from unittest.mock import Mock


class TestConfigureMonitorCapture(TestCase):

    def test_configure_monitor_capture(self):
        self.device = Mock()
        results_map = {
            'monitor capture capture_name match any interface FortyGigabitEthernet1/0/1 both file location flash:capture_name size 70 buffer-size 5 limit duration 100 packets 1000 packet-len 64 every 1000 pps 100000': 
            'Interface FortyGigabitEthernet1/0/1 direction BOTH is already attached to the capture '
            'A filter is already attached to the capture. Replace with specified filter?[confirm] '
            'Duration limit is already set, replace?[confirm] ' 
            'Packet Size limit is already set, replace?[confirm] '
            'Packet count limit is already set, replace?[confirm] '
            'Packets per second limit is already set, replace?[confirm] '
            'Packet sampling limit is already set, replace?[confirm] '
            'A file name has already been associated, replace?[confirm] '
            'Buffer size was  already specified, replace?[confirm] '
            'File size was already specified, replace?[confirm]'
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = configure_monitor_capture(self.device, 'capture_name', 'any', 'both', 'FortyGigabitEthernet1/0/1', 'flash:capture_name', 70, 5, 100, 1000, 64, 1000, 100000)
        self.assertIn(
            'monitor capture capture_name match any interface FortyGigabitEthernet1/0/1 both file location flash:capture_name size 70 buffer-size 5 limit duration 100 packets 1000 packet-len 64 every 1000 pps 100000',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
