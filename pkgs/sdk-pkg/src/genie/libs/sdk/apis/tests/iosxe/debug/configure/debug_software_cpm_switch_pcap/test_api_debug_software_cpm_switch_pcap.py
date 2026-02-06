from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.debug.configure import debug_software_cpm_switch_pcap


class TestDebugSoftwareCpmSwitchPcap(TestCase):
    def test_debug_software_cpm_switch_pcap(self):
        device = Mock()
        result = debug_software_cpm_switch_pcap(device, '1', 'enable', True)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('debug platform software cpm switch 1 bp active pcap enable',)
        )