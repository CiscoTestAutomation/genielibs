from unittest import TestCase
from genie.libs.sdk.apis.iosxe.utils import sweep_ping
from unittest.mock import Mock


class TestSweepPing(TestCase):

    def test_sweep_ping(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.ping = Mock(return_value="""
        sweep ping for ip 177.1.1.2 on whitneyx_09
        
        2026-01-30 01:49:18,260: %UNICON-INFO: +++ whitneyx_09(alias=uut) with via 'cli': ping +++
        ping
        Protocol [ip]: ip
        Target IP address: 177.1.1.2
        Repeat count [5]: 1
        Datagram size [100]:
        Timeout in seconds [2]: 5
        Extended commands [n]: y
        Ingress ping [n]:
        Source address or interface:
        DSCP Value [0]:
        Type of service [0]:
        Set DF bit in IP header? [no]: n
        Validate reply data? [no]:
        Data pattern [0x0000ABCD]:
        Loose, Strict, Record, Timestamp, Verbose[none]: v
        Loose, Strict, Record, Timestamp, Verbose[V]:
        Sweep range of sizes [n]: y
        Sweep min size [36]: 48
        Sweep max size [18024]: 1000
        Sweep interval [1]: 10
        Type escape sequence to abort.
        Sending 96, [48..1000]-byte ICMP Echos to 177.1.1.2, timeout is 5 seconds:
        Reply to request 0 (1 ms) (size 48)
        Reply to request 1 (1 ms) (size 58)
        Reply to request 2 (1 ms) (size 68)
        Reply to request 3 (1 ms) (size 78)
        Reply to request 4 (1 ms) (size 88)
        Reply to request 5 (1 ms) (size 98)
        Reply to request 6 (4 ms) (size 108)
        Reply to request 7 (1 ms) (size 118)
        Reply to request 8 (1 ms) (size 128)
        Reply to request 9 (1 ms) (size 138)
        Reply to request 10 (1 ms) (size 148)
        Reply to request 11 (1 ms) (size 158)
        Reply to request 12 (1 ms) (size 168)
        Reply to request 13 (1 ms) (size 178)
        Reply to request 14 (4 ms) (size 188)
        Reply to request 15 (1 ms) (size 198)
        Reply to request 16 (1 ms) (size 208)
        Reply to request 17 (1 ms) (size 218)
        Reply to request 18 (1 ms) (size 228)
        Reply to request 19 (1 ms) (size 238)
        Reply to request 20 (1 ms) (size 248)
        Reply to request 21 (1 ms) (size 258)
        Reply to request 22 (4 ms) (size 268)
        Reply to request 23 (1 ms) (size 278)
        Reply to request 24 (1 ms) (size 288)
        Reply to request 25 (1 ms) (size 298)
        Reply to request 26 (1 ms) (size 308)
        Reply to request 27 (1 ms) (size 318)
        Reply to request 28 (4 ms) (size 328)
        Reply to request 29 (1 ms) (size 338)
        Reply to request 30 (1 ms) (size 348)
        Reply to request 31 (1 ms) (size 358)
        Reply to request 32 (1 ms) (size 368)
        Reply to request 33 (1 ms) (size 378)
        Reply to request 34 (1 ms) (size 388)
        Reply to request 35 (1 ms) (size 398)
        Reply to request 36 (4 ms) (size 408)
        Reply to request 37 (1 ms) (size 418)
        Reply to request 38 (1 ms) (size 428)
        Reply to request 39 (1 ms) (size 438)
        Reply to request 40 (1 ms) (size 448)
        Reply to request 41 (1 ms) (size 458)
        Reply to request 42 (1 ms) (size 468)
        Reply to request 43 (1 ms) (size 478)
        Reply to request 44 (4 ms) (size 488)
        Reply to request 45 (1 ms) (size 498)
        Reply to request 46 (1 ms) (size 508)
        Reply to request 47 (1 ms) (size 518)
        Reply to request 48 (1 ms) (size 528)
        Reply to request 49 (1 ms) (size 538)
        Reply to request 50 (1 ms) (size 548)
        Reply to request 51 (1 ms) (size 558)
        Reply to request 52 (4 ms) (size 568)
        Reply to request 53 (1 ms) (size 578)
        Reply to request 54 (1 ms) (size 588)
        Reply to request 55 (1 ms) (size 598)
        Reply to request 56 (1 ms) (size 608)
        Reply to request 57 (1 ms) (size 618)
        Reply to request 58 (1 ms) (size 628)
        Reply to request 59 (1 ms) (size 638)
        Reply to request 60 (4 ms) (size 648)
        Reply to request 61 (1 ms) (size 658)
        Reply to request 62 (1 ms) (size 668)
        Reply to request 63 (1 ms) (size 678)
        Reply to request 64 (1 ms) (size 688)
        Reply to request 65 (1 ms) (size 698)
        Reply to request 66 (1 ms) (size 708)
        Reply to request 67 (1 ms) (size 718)
        Reply to request 68 (4 ms) (size 728)
        Reply to request 69 (1 ms) (size 738)
        Reply to request 70 (1 ms) (size 748)
        Reply to request 71 (1 ms) (size 758)
        Reply to request 72 (1 ms) (size 768)
        Reply to request 73 (1 ms) (size 778)
        Reply to request 74 (1 ms) (size 788)
        Reply to request 75 (1 ms) (size 798)
        Reply to request 76 (4 ms) (size 808)
        Reply to request 77 (1 ms) (size 818)
        Reply to request 78 (1 ms) (size 828)
        Reply to request 79 (1 ms) (size 838)
        Reply to request 80 (1 ms) (size 848)
        Reply to request 81 (1 ms) (size 858)
        Reply to request 82 (1 ms) (size 868)
        Reply to request 83 (1 ms) (size 878)
        Reply to request 84 (4 ms) (size 888)
        Reply to request 85 (1 ms) (size 898)
        Reply to request 86 (1 ms) (size 908)
        Reply to request 87 (1 ms) (size 918)
        Reply to request 88 (1 ms) (size 928)
        Reply to request 89 (1 ms) (size 938)
        Reply to request 90 (1 ms) (size 948)
        Reply to request 91 (4 ms) (size 958)
        Reply to request 92 (1 ms) (size 968)
        Reply to request 93 (1 ms) (size 978)
        Reply to request 94 (1 ms) (size 988)
        Reply to request 95 (1 ms) (size 998)
        Success rate is 100 percent (96/96), round-trip min/avg/max = 1/1/4 ms
        whitneyx_09#
        """)
        expected_output = True
        actual_output = sweep_ping(self.device, '177.1.1.2', 'ip', 100, 100, 'n', 48, 1000, 10, 300, 'y')
        expected_output = True
        self.assertEqual(actual_output, expected_output)


        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.ping = Mock(return_value="""
        sweep ping for ip 2001:177:1:1::2 on whitneyx_09
        
        2026-01-30 01:20:22,730: %UNICON-INFO: +++ whitneyx_09(alias=uut) with via 'cli': ping +++
        ping
        Protocol [ip]: ipv6
        Target IPv6 address: 2001:177:1:1::2
        Repeat count [5]: 1
        Datagram size [100]:
        Timeout in seconds [2]: 5
        Extended commands? [no]: y
        Source address or interface:
        UDP protocol? [no]:
        Verbose? [no]:
        Precedence [0]:
        DSCP [0]:
        Include hop by hop option? [no]:
        Include destination option? [no]:
        Sweep range of sizes? [no]: y
        Sweep min size [48]: 48
        Sweep max size [18024]: 1000
        Sweep interval [1]: 10
        Type escape sequence to abort.
        Sending 96, [48..1000]-byte ICMP Echos to 2001:177:1:1::2, timeout is 5 seconds:
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!
        Success rate is 100 percent (96/96), round-trip min/avg/max = 1/1/4 ms
        whitneyx_09#
        """)
        expected_output = True
        actual_output = sweep_ping(self.device, '2001:177:1:1::2', 'ipv6', 100, 100, 'n', 48, 1000, 10, 300, 'n')
        expected_output = True
        self.assertEqual(actual_output, expected_output)