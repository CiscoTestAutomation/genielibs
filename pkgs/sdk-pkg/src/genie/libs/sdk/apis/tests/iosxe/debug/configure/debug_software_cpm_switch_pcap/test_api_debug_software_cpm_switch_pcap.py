from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_software_cpm_switch_pcap
from unittest.mock import Mock


class TestDebugSoftwareCpmSwitchPcap(TestCase):

    def test_debug_software_cpm_switch_pcap(self):
        self.device = Mock()
        results_map = {
            'debug platform software cpm switch 1 bp active pcap enable': 'Enabling CPM packet capture',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = debug_software_cpm_switch_pcap(self.device, '1', 'enable', True)
        self.assertIn(
            'debug platform software cpm switch 1 bp active pcap enable',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
