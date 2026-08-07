from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import configure_monitor_capture
from unittest.mock import Mock


class TestConfigureMonitorCapture(TestCase):

    def _run(self, **kwargs):
        device = Mock()
        device.execute.return_value = ''
        configure_monitor_capture(
            device, 'cap', 'any', 'both', 'GigabitEthernet1/0/1', **kwargs)
        return device.execute.call_args_list[0][0][0]

    def test_minimal(self):
        self.assertEqual(
            self._run(),
            'monitor capture cap match any interface GigabitEthernet1/0/1 both')

    def test_buffer_limit(self):
        self.assertEqual(
            self._run(buffer_size=100, duration=60, packets=5000),
            'monitor capture cap match any interface GigabitEthernet1/0/1 both '
            'buffer size 100 limit duration 60 packets 5000')

    def test_buffer_packets_only(self):
        self.assertEqual(
            self._run(buffer_size=100, packets=5000),
            'monitor capture cap match any interface GigabitEthernet1/0/1 both '
            'buffer size 100 limit packets 5000')

    def test_file_location_size(self):
        self.assertEqual(
            self._run(file_location='flash:capt.pcap', file_size=50),
            'monitor capture cap match any interface GigabitEthernet1/0/1 both '
            'file location flash:capt.pcap size 50')

    def test_file_size_without_location_dropped(self):
        self.assertEqual(
            self._run(file_size=50),
            'monitor capture cap match any interface GigabitEthernet1/0/1 both')

    def test_all_limit_subopts(self):
        self.assertEqual(
            self._run(buffer_size=100, duration=60, packets=5000,
                      packet_len=128, capture_frequency=10, pps=100),
            'monitor capture cap match any interface GigabitEthernet1/0/1 both '
            'buffer size 100 limit duration 60 packets 5000 packet-len 128 '
            'every 10 pps 100')
