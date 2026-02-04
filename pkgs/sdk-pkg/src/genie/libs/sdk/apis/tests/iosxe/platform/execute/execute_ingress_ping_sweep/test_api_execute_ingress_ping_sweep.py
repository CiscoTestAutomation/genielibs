from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_ingress_ping_sweep
from unittest.mock import Mock


class TestExecuteIngressPingSweep(TestCase):

    def test_execute_ingress_ping_sweep(self):
        self.device = Mock()
        results_map = {
            'ping': '''Protocol [ip]: ip
Target IP address: 11.1.0.2
Repeat count [5]: 5
Datagram size [100]: 100
Timeout in seconds [2]: 
Extended commands [n]: y
Ingress ping [n]: y
Ingress interface: GigabitEthernet0/0/0
DSCP Value [0]: 0
Type of service [0]: 
Set DF bit in IP header? [no]: 
Validate reply data? [no]: 
Data pattern [0x0000ABCD]: 
Loose, Strict, Record, Timestamp, Verbose[none]: 
Sweep range of sizes [n]: y
Sweep min size [36]: 36
Sweep max size [18024]: 100
Sweep interval [1]: 1
Type escape sequence to abort.
Sending 325, [36..100]-byte ICMP Echos to 11.1.0.2, timeout is 2 seconds:
Packet sent with a source address of 11.0.0.1 
......................................................................
......................................................................
......................................................................
......................................................................
.............................................
Success rate is 0 percent (0/325)''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_ingress_ping_sweep(self.device, '11.1.0.2', 'GigabitEthernet0/0/0', 36, 100, 1, 5, 100, 0, 1800, 2, 0, False, False, None)
        self.assertIn(
            'ping',
            self.device.execute.call_args_list[0][0]
        )
        self.assertIsNotNone(result)
        self.assertIn('Success rate is 0 percent (0/325)', result)
