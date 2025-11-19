from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.get import get_show_flow_monitor_cache_format_table_output
from unittest.mock import Mock


class TestGetShowFlowMonitorCacheFormatTableOutput(TestCase):

    def test_get_show_flow_monitor_cache_format_table_output(self):
        self.device = Mock()
        results_map = {
            'show flow monitor ipv4_monitor_in cache format table': (
            '  Cache type:                               Normal (Platform cache)\r\n'
            '  Cache size:                                40000\r\n'
            '  Current entries:                               1\r\n'
            '\r\n'
            '  Flows added:                                  15\r\n'
            '  Flows aged:                                   14\r\n'
            '    - Active timeout      (    60 secs)         14\r\n'
            '\r\n'
            'IPV4 SRC ADDR    IPV4 DST ADDR    ICMP IPV4 TYPE  ICMP IPV4 CODE  INTF INPUT            IP PROT             pkts long  time abs first  time abs last     bytes layer2 long\r\n'
            '===============  ===============  ==============  ==============  ====================  =======  ====================  ==============  =============  ====================\r\n'
            '10.10.10.2       10.10.10.1                    8               0  Po10                        1                     7    12:10:48.219   12:10:55.020                     0'
            ),
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = get_show_flow_monitor_cache_format_table_output(self.device, 'ipv4_monitor_in', 180)
        self.assertIn(
            'show flow monitor ipv4_monitor_in cache format table',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = (
 '  Cache type:                               Normal (Platform cache)\r\n'
 '  Cache size:                                40000\r\n'
 '  Current entries:                               1\r\n'
 '\r\n'
 '  Flows added:                                  15\r\n'
 '  Flows aged:                                   14\r\n'
 '    - Active timeout      (    60 secs)         14\r\n'
 '\r\n'
 'IPV4 SRC ADDR    IPV4 DST ADDR    ICMP IPV4 TYPE  ICMP IPV4 CODE  INTF '
 'INPUT            IP PROT             pkts long  time abs first  time abs '
 'last     bytes layer2 long\r\n'
 '===============  ===============  ==============  ==============  '
 '====================  =======  ====================  ==============  '
 '=============  ====================\r\n'
 '10.10.10.2       10.10.10.1                    8               0  '
 'Po10                        1                     7    12:10:48.219   '
 '12:10:55.020                     0')
        self.assertEqual(result, expected_output)