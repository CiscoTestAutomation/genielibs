from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_software_cpm_switch_pcap_drop
from unittest.mock import Mock


class TestDebugSoftwareCpmSwitchPcapDrop(TestCase):

    def test_debug_software_cpm_switch_pcap_drop(self):
        self.device = Mock()
        results_map = {
            'debug platform software cpm switch 2 b0 pcap drop enable': 'Enabling pcap drop capture',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = debug_software_cpm_switch_pcap_drop(self.device, '2', 'enable', False)
        self.assertIn(
            'debug platform software cpm switch 2 b0 pcap drop enable',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
