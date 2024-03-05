import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_information


class TestGetInterfaceInformation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_information(self):
        result = get_interface_information(self.device, ['GigabitEthernet1'])
        expected_output = {'GigabitEthernet1': {'arp_timeout': '04:00:00',
                                           'arp_type': 'arpa',
                                           'auto_negotiate': True,
                                           'bandwidth': 1000000,
                                           'counters': {'in_broadcast_pkts': 0,
                                                        'in_crc_errors': 0,
                                                        'in_errors': 0,
                                                        'in_frame': 0,
                                                        'in_giants': 0,
                                                        'in_ignored': 0,
                                                        'in_mac_pause_frames': 0,
                                                        'in_multicast_pkts': 0,
                                                        'in_no_buffer': 0,
                                                        'in_octets': 57084695479,
                                                        'in_overrun': 0,
                                                        'in_pkts': 346976186,
                                                        'in_runts': 0,
                                                        'in_throttles': 0,
                                                        'in_watchdog': 0,
                                                        'last_clear': 'never',
                                                        'out_babble': 0,
                                                        'out_buffer_failure': 0,
                                                        'out_buffers_swapped': 0,
                                                        'out_collision': 0,
                                                        'out_deferred': 0,
                                                        'out_errors': 0,
                                                        'out_interface_resets': 1,
                                                        'out_late_collision': 0,
                                                        'out_lost_carrier': 0,
                                                        'out_mac_pause_frames': 0,
                                                        'out_no_carrier': 0,
                                                        'out_octets': 53171615,
                                                        'out_pkts': 307566,
                                                        'out_underruns': 0,
                                                        'out_unknown_protocl_drops': 243052,
                                                        'rate': {'in_rate': 181000,
                                                                 'in_rate_pkts': 140,
                                                                 'load_interval': 300,
                                                                 'out_rate': 0,
                                                                 'out_rate_pkts': 0}},
                                           'delay': 10,
                                           'duplex_mode': 'full',
                                           'enabled': True,
                                           'encapsulations': {'encapsulation': 'arpa'},
                                           'flow_control': {'receive': False,
                                                            'send': False},
                                           'ipv4': {'172.16.1.211/24': {'ip': '172.16.1.211',
                                                                        'prefix_length': '24'}},
                                           'is_deleted': False,
                                           'keepalive': 10,
                                           'last_input': '00:00:00',
                                           'last_output': '00:00:22',
                                           'line_protocol': 'up',
                                           'link_type': 'auto',
                                           'mac_address': '5e01.4000.0000',
                                           'media_type': 'Virtual',
                                           'mtu': 1500,
                                           'oper_status': 'up',
                                           'output_hang': 'never',
                                           'phys_address': '5e01.4000.0000',
                                           'port_channel': {'port_channel_member': False},
                                           'port_speed': '1000mbps',
                                           'queues': {'input_queue_drops': 0,
                                                      'input_queue_flushes': 0,
                                                      'input_queue_max': 375,
                                                      'input_queue_size': 0,
                                                      'output_queue_max': 40,
                                                      'output_queue_size': 0,
                                                      'queue_strategy': 'fifo',
                                                      'total_output_drop': 0},
                                           'reliability': '255/255',
                                           'rxload': '1/255',
                                           'txload': '1/255',
                                           'type': 'CSR vNIC'}}
        self.assertEqual(result, expected_output)
