from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_software_cpm_switch_pcap_count
from unittest.mock import Mock


class TestDebugSoftwareCpmSwitchPcapCount(TestCase):

    def test_debug_software_cpm_switch_pcap_count(self):
        self.device = Mock()
        results_map = {
            'debug platform software cpm switch 1 b0 pcap count 2': 'Changing packet buffer size from 5 to 2',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = debug_software_cpm_switch_pcap_count(self.device, '1', 2, False)
        self.assertIn(
            'debug platform software cpm switch 1 b0 pcap count 2',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
