from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_controller_output
from unittest.mock import Mock


class TestGetInterfaceControllerOutput(TestCase):

    def test_get_interface_controller_output(self):
        self.device = Mock()
        results_map = {
            'show interface GigabitEthernet0/1/5 controller':
            '''GigabitEthernet0/1/5 is down, line protocol is down (notconnect) 
            Hardware is C1126-ES-8, address is 10e3.7677.310d (bia 10e3.7677.310d)
            MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec, 
                reliability 255/255, txload 1/255, rxload 1/255
            Encapsulation ARPA, loopback not set
            Keepalive not supported 
            Auto-duplex, Auto-speed, link type is auto, media type is 10/100/1000BaseTX
            input flow-control is off, output flow-control is unsupported 
            ARP type: ARPA, ARP Timeout 04:00:00
            Last input never, output never, output hang never
            Last clearing of "show interface" counters never
            Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
            Queueing strategy: fifo
            Output queue: 0/40 (size/max)
            5 minute input rate 0 bits/sec, 0 packets/sec
            5 minute output rate 0 bits/sec, 0 packets/sec
                0 packets input, 0 bytes, 0 no buffer
                Received 0 broadcasts (0 multicasts)
                0 runts, 0 giants, 0 throttles 
                0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
                0 watchdog, 0 multicast, 0 pause input
                0 input packets with dribble condition detected
                0 packets output, 0 bytes, 0 underruns
                Output 0 broadcasts (0 multicasts)
                0 output errors, 0 collisions, 54 interface resets
                0 unknown protocol drops
                0 babbles, 0 late collision, 0 deferred
                0 lost carrier, 0 no carrier, 0 pause output
                0 output buffer failures, 0 output buffers swapped out

            GE5: iid 0
            mac status: lport 5, speed 10, duplex half, link down, forcedlink disabled, forcedfc disabled
            L2_NETWORK
            link down(config enabled), speed unknown(config auto), duplex unknown(config auto), config autoneg, mtu 1526
            rx_pause off(config off), tx_pause off(config off)
            vlan mode access, native vlan 1
            qos mode trust, default priority 0
            mac learning auto learning, protected port disabled




            GE5 Statistics:
            Input:
                pkts 0, bytes 0
                unicast 0, multicast 0, broadcast 0
                total drops 0, total errors 0, overrun 0, crc 0
                pkts64 0, pkts65to127 0, pkts128to255 0, 
                pkts256to511 0, pkts512to1023 0, pkts1024toMax 0
                oversize 0, undersize 0, jabber 0, fragments 0, 
                collision 0, pause 0, align 0
            Output:
                pkts 0, bytes 0, 
                unicast 0, multicast 0, broadcast 0
                total drops 0, total errors 0, underrun 0
                collision 0, pause 0
                defer 0, late 0, excessive 0, fcs 0
            ATU LearnLimit: 0, LearnCnt: 0
            RxQ rsvd: 0, cnt: 0, XON Limit: 19, XOFF Limit: 250
            TxQ total cnt: 0
            TxQ 0 cnt: 0
            TxQ 1 cnt: 0
            TxQ 2 cnt: 0
            TxQ 3 cnt: 0
            TxQ 4 cnt: 0
            TxQ 5 cnt: 0
            TxQ 6 cnt: 0
            TxQ 7 cnt: 0



            switch smi access, multi-chipset mode''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = get_interface_controller_output(self.device, 'GigabitEthernet0/1/5')
        self.assertIn(
            'show interface GigabitEthernet0/1/5 controller',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = results_map['show interface GigabitEthernet0/1/5 controller']
        self.assertEqual(result, expected_output)
