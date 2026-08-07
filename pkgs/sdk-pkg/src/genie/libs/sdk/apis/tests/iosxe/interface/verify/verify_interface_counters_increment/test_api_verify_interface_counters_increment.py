import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.interface.verify import (
    verify_interface_counters_increment)


def _get_counter(interface, counter_field, output):
    """Read the real counter value from the parsed output."""
    return output[interface]['counters'].get(counter_field)


class TestVerifyInterfaceCountersIncrement(unittest.TestCase):

    def setUp(self):
        # Full parsed output of:
        # show interfaces GigabitEthernet0/0/0
        self.intf_output = {
            'GigabitEthernet0/0/0': {
                'oper_status': 'down',
                'line_protocol': 'down',
                'enabled': False,
                'connected': False,
                'type': 'C8221-8T2X',
                'mac_address': '44c2.0c82.0f60',
                'phys_address': '44c2.0c82.0f60',
                'mtu': 1500,
                'bandwidth': 1000000,
                'delay': 10,
                'reliability': '255/255',
                'txload': '1/255',
                'rxload': '1/255',
                'encapsulations': {
                    'encapsulation': 'arpa',
                },
                'auto_negotiate': True,
                'duplex_mode': 'auto',
                'port_speed': 'auto',
                'link_type': 'auto',
                'media_type': '10/100/1000BaseTX',
                'flow_control': {
                    'receive': False,
                    'send': False,
                },
                'arp_type': 'arpa',
                'arp_timeout': '04:00:00',
                'last_input': '5w0d',
                'last_output': '5w0d',
                'output_hang': 'never',
                'queues': {
                    'input_queue_size': 0,
                    'input_queue_max': 375,
                    'input_queue_drops': 0,
                    'input_queue_flushes': 0,
                    'total_output_drop': 0,
                    'queue_strategy': 'fifo',
                    'output_queue_size': 0,
                    'output_queue_max': 40,
                },
                'counters': {
                    'rate': {
                        'load_interval': 300,
                        'in_rate': 0,
                        'in_rate_pkts': 0,
                        'out_rate': 0,
                        'out_rate_pkts': 0,
                    },
                    'last_clear': 'never',
                    'in_pkts': 456,
                    'in_octets': 76326,
                    'in_no_buffer': 0,
                    'in_broadcast_pkts': 302,
                    'in_multicast_pkts': 142,
                    'in_runts': 0,
                    'in_giants': 0,
                    'in_throttles': 0,
                    'in_errors': 0,
                    'in_crc_errors': 0,
                    'in_frame': 0,
                    'in_overrun': 0,
                    'in_ignored': 0,
                    'in_watchdog': 0,
                    'in_mac_pause_frames': 0,
                    'in_with_dribble': 0,
                    'out_pkts': 1267,
                    'out_octets': 440031,
                    'out_underruns': 0,
                    'out_broadcast_pkts': 30,
                    'out_multicast_pkts': 1231,
                    'out_errors': 0,
                    'out_collision': 0,
                    'out_interface_resets': 45,
                    'out_unknown_protocl_drops': 0,
                    'out_babble': 0,
                    'out_late_collision': 0,
                    'out_deferred': 0,
                    'out_lost_carrier': 28,
                    'out_no_carrier': 0,
                    'out_mac_pause_frames': 0,
                    'out_buffer_failure': 0,
                    'out_buffers_swapped': 0,
                },
            }
        }

    def _make_device(self, intf_output):
        device = Mock()
        device.api.get_show_interface_output = Mock(
            return_value=intf_output)
        device.api.get_interface_packet_counter = Mock(
            side_effect=_get_counter)
        return device

    def test_out_pkts_increment_pass_no_max(self):
        # out_pkts=1267, before=1000, increment=267 >= 100
        device = self._make_device(self.intf_output)
        result = verify_interface_counters_increment(
            device, 'GigabitEthernet0/0/0', 'out_pkts',
            before_value=1000, expect_increment_min=100,
            max_time=1, check_interval=1)
        self.assertTrue(result)

    def test_in_pkts_increment_pass_within_max(self):
        # in_pkts=456, before=400, increment=56 in [10, 100]
        device = self._make_device(self.intf_output)
        result = verify_interface_counters_increment(
            device, 'GigabitEthernet0/0/0', 'in_pkts',
            before_value=400, expect_increment_min=10,
            expect_increment_max=100, max_time=1,
            check_interval=1)
        self.assertTrue(result)

    def test_out_pkts_increment_above_max(self):
        # out_pkts=1267, before=1000, increment=267 > 100
        device = self._make_device(self.intf_output)
        result = verify_interface_counters_increment(
            device, 'GigabitEthernet0/0/0', 'out_pkts',
            before_value=1000, expect_increment_min=10,
            expect_increment_max=100, max_time=1,
            check_interval=1)
        self.assertFalse(result)

    def test_in_pkts_increment_below_min(self):
        # in_pkts=456, before=400, increment=56 < 1000
        device = self._make_device(self.intf_output)
        result = verify_interface_counters_increment(
            device, 'GigabitEthernet0/0/0', 'in_pkts',
            before_value=400, expect_increment_min=1000,
            max_time=1, check_interval=1)
        self.assertFalse(result)

    def test_no_interface_output(self):
        device = self._make_device(None)
        result = verify_interface_counters_increment(
            device, 'GigabitEthernet0/0/0', 'out_pkts',
            before_value=1000, expect_increment_min=10,
            max_time=1, check_interval=1)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
