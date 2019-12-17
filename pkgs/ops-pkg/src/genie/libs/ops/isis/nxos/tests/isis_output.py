""" 
Isis Genie Ops Object Outputs for IOSXE.
"""


class IsisOutput(object):
    
    showIsisVrfAll = '''\
        show isis vrf all

        ISIS process : test
        Instance number :  1
        UUID: 1090519320
        Process ID 1326
        VRF: default
        System ID : 7777.7777.7777  IS-Type : L1-L2
        SAP : 412  Queue Handle : 15
        Maximum LSP MTU: 1492
        Stateful HA enabled
        Graceful Restart enabled. State: Inactive
        Last graceful restart status : none
        Start-Mode Complete
        BFD IPv4 is globally disabled for ISIS process: test
        BFD IPv6 is globally disabled for ISIS process: test
        Topology-mode is Multitopology
        Metric-style : advertise(wide), accept(narrow, wide)
        Area address(es) :
            49.0002
        Process is up and running
        VRF ID: 1
        Stale routes during non-graceful controlled restart
        Enable resolution of L3->L2 address for ISIS adjacency
        SR IPv4 is not configured and disabled for ISIS process: test
        SR IPv6 is not configured and disabled for ISIS process: test
        Interfaces supported by IS-IS :
            loopback0
            Ethernet1/1
            Ethernet1/2
            Ethernet1/3
            Ethernet1/4
        Topology : 0
        Address family IPv4 unicast :
            Number of interface : 5
            Distance : 115
        Address family IPv6 unicast :
            Number of interface : 0
            Distance : 115
        Topology : 2
        Address family IPv6 unicast :
            Number of interface : 5
            Distance : 115
        Level1
        No auth type and keychain
        Auth check set
        Level2
        No auth type and keychain
        Auth check set
        L1 Next SPF: 00:00:06
        L2 Next SPF: 00:00:02

        ISIS process : test
        Instance number :  1
        UUID: 1090519320
        Process ID 1326
        VRF: VRF1
        System ID : 7777.7777.7777  IS-Type : L1-L2
        SAP : 412  Queue Handle : 15
        Maximum LSP MTU: 1492
        Stateful HA enabled
        Graceful Restart enabled. State: Inactive
        Last graceful restart status : none
        Start-Mode Complete
        BFD IPv4 is globally disabled for ISIS process: test
        BFD IPv6 is globally disabled for ISIS process: test
        Topology-mode is Multitopology
        Metric-style : advertise(wide), accept(narrow, wide)
        Area address(es) :
            49.0002
        Process is up and running
        VRF ID: 3
        Stale routes during non-graceful controlled restart
        Enable resolution of L3->L2 address for ISIS adjacency
        SR IPv4 is not configured and disabled for ISIS process: test
        SR IPv6 is not configured and disabled for ISIS process: test
        Interfaces supported by IS-IS :
            loopback1
            Ethernet1/5
        Topology : 0
        Address family IPv4 unicast :
            Number of interface : 2
            Distance : 115
        Address family IPv6 unicast :
            Number of interface : 0
            Distance : 115
        Topology : 2
        Address family IPv6 unicast :
            Number of interface : 2
            Distance : 115
        Level1
        No auth type and keychain
        Auth check set
        Level2
        No auth type and keychain
        Auth check set
        L1 Next SPF: Inactive
        L2 Next SPF: 00:00:05
    '''

    showIsisInterfaceVrfAll = '''\
        show isis interface vrf all
        IS-IS process: test VRF: default
        loopback0, Interface status: protocol-up/link-up/admin-up
        IP address: 7.7.7.7, IP subnet: 7.7.7.7/32
        IPv6 address:
            2001:db8:7:7:7::7/128 [VALID]
        IPv6 subnet:  2001:db8:7:7:7::7/128
        IPv6 link-local address: fe80::5c00:40ff:fe06:0
        Level1
            No auth type and keychain
            Auth check set
        Level2
            No auth type and keychain
            Auth check set
        Index: 0x0001, Local Circuit ID: 0x01, Circuit Type: L1-2
        BFD IPv4 is locally disabled for Interface loopback0
        BFD IPv6 is locally disabled for Interface loopback0
        MTR is enabled
        Level      Metric
        1               1
        2               1
        Topologies enabled:
            L  MT  Metric  MetricCfg  Fwdng IPV4-MT  IPV4Cfg  IPV6-MT  IPV6Cfg
            1  0        1       no   UP    UP       yes      DN       yes
            1  2        1       no   UP    DN       no       UP       yes
            2  0        1       no   UP    UP       yes      DN       yes
            2  2        1       no   UP    DN       no       UP       yes

        Ethernet1/1, Interface status: protocol-up/link-up/admin-up
        IP address: 10.5.7.7, IP subnet: 10.5.7.0/24
        IPv6 address:
            2001:db8:10:5:7::7/64 [VALID]
        IPv6 subnet:  2001:db8:10:5::/64
        IPv6 link-local address: fe80::5c00:40ff:fe06:7
        Level1
            No auth type and keychain
            Auth check set
        Level2
            No auth type and keychain
            Auth check set
        Index: 0x0002, Local Circuit ID: 0x01, Circuit Type: L1-2
        BFD IPv4 is locally disabled for Interface Ethernet1/1
        BFD IPv6 is locally disabled for Interface Ethernet1/1
        MTR is enabled
        Passive level: level-1-2
        LSP interval: 33 ms, MTU: 1500
        Level-1 Designated IS: R5
        Level-2 Designated IS: R5
        Level   Metric-0   Metric-2   CSNP  Next CSNP  Hello   Multi   Next IIH
        1              40     40     10 00:00:02      10   3       00:00:05
        2              40     40     10 00:00:08      10   3       00:00:05
        Level  Adjs   AdjsUp Pri  Circuit ID         Since
        1         1        1  64  R5.03              1w0d
        2         1        1  64  R5.03              1w0d
        Topologies enabled:
            L  MT  Metric  MetricCfg  Fwdng IPV4-MT  IPV4Cfg  IPV6-MT  IPV6Cfg
            1  0        40      no   UP    UP       yes      DN       yes
            1  2        40      no   UP    DN       no       UP       yes
            2  0        40      no   UP    UP       yes      DN       yes
            2  2        40      no   UP    DN       no       UP       yes

        Ethernet1/2, Interface status: protocol-up/link-up/admin-up
        IP address: 10.6.7.7, IP subnet: 10.6.7.0/24
        IPv6 address:
            2001:db8:10:6:7::7/64 [VALID]
        IPv6 subnet:  2001:db8:10:6::/64
        IPv6 link-local address: fe80::5c00:40ff:fe06:7
        Level1
            No auth type and keychain
            Auth check set
        Level2
            No auth type and keychain
            Auth check set
        Index: 0x0003, Local Circuit ID: 0x02, Circuit Type: L1
        BFD IPv4 is locally disabled for Interface Ethernet1/2
        BFD IPv6 is locally disabled for Interface Ethernet1/2
        MTR is enabled
        LSP interval: 33 ms, MTU: 1500
        Level-1 Designated IS: R7
        Level   Metric-0   Metric-2   CSNP  Next CSNP  Hello   Multi   Next IIH
        1              40     40     10 0.788413       3   3       0.589815
        2              40     40     10 Inactive      10   3       Inactive
        Level  Adjs   AdjsUp Pri  Circuit ID         Since
        1         1        1  64  R7.02            * 1w0d
        2         0        0  64  0000.0000.0000.00  never
        Topologies enabled:
            L  MT  Metric  MetricCfg  Fwdng IPV4-MT  IPV4Cfg  IPV6-MT  IPV6Cfg
            1  0        40      no   UP    UP       yes      DN       yes
            1  2        40      no   UP    DN       no       UP       yes
            2  0        40      no   UP    DN       no       DN       no
            2  2        40      no   UP    DN       no       DN       no

        Ethernet1/3, Interface status: protocol-up/link-up/admin-up
        IP address: 10.7.8.7, IP subnet: 10.7.8.0/24
        IPv6 address:
            2001:db8:10:7:8::7/64 [VALID]
        IPv6 subnet:  2001:db8:10:7::/64
        IPv6 link-local address: fe80::5c00:40ff:fe06:7
        Level1
            No auth type and keychain
            Auth check set
        Level2
            No auth type and keychain
            Auth check set
        Index: 0x0004, Local Circuit ID: 0x03, Circuit Type: L2
        BFD IPv4 is locally disabled for Interface Ethernet1/3
        BFD IPv6 is locally disabled for Interface Ethernet1/3
        MTR is enabled
        LSP interval: 33 ms, MTU: 1500
        Level-2 Designated IS: R8
        Level   Metric-0   Metric-2   CSNP  Next CSNP  Hello   Multi   Next IIH
        1              40     40     10 Inactive      10   3       Inactive
        2              40     40     10 00:00:05      10   3       00:00:04
        Level  Adjs   AdjsUp Pri  Circuit ID         Since
        1         0        0  64  0000.0000.0000.00  never
        2         1        1  64  R8.01              1w0d
        Topologies enabled:
            L  MT  Metric  MetricCfg  Fwdng IPV4-MT  IPV4Cfg  IPV6-MT  IPV6Cfg
            1  0        40      no   UP    DN       no       DN       no
            1  2        40      no   UP    DN       no       DN       no
            2  0        40      no   UP    UP       yes      DN       yes
            2  2        40      no   UP    DN       no       UP       yes

        Ethernet1/4, Interface status: protocol-up/link-up/admin-up
        IP address: 10.7.9.7, IP subnet: 10.7.9.0/24
        IPv6 address:
            2001:db8:10:77:9::7/64 [VALID]
        IPv6 subnet:  2001:db8:10:77::/64
        IPv6 link-local address: fe80::5c00:40ff:fe06:7
        Level1
            No auth type and keychain
            Auth check set
        Level2
            No auth type and keychain
            Auth check set
        Index: 0x0005, Local Circuit ID: 0x04, Circuit Type: L1-2
        BFD IPv4 is locally disabled for Interface Ethernet1/4
        BFD IPv6 is locally disabled for Interface Ethernet1/4
        MTR is enabled
        LSP interval: 33 ms, MTU: 1500
        Level-2 Designated IS: R9
        Level   Metric-0   Metric-2   CSNP  Next CSNP  Hello   Multi   Next IIH
        1              40     40     10 Inactive      10   3       00:00:04
        2              40     40     10 00:00:03      10   3       0.911618
        Level  Adjs   AdjsUp Pri  Circuit ID         Since
        1         0        0  64  R7.04              never
        2         1        1  64  R9.01              1w0d
        Topologies enabled:
            L  MT  Metric  MetricCfg  Fwdng IPV4-MT  IPV4Cfg  IPV6-MT  IPV6Cfg
            1  0        40      no   UP    UP       yes      DN       yes
            1  2        40      no   UP    DN       no       UP       yes
            2  0        40      no   UP    UP       yes      DN       yes
            2  2        40      no   UP    DN       no       UP       yes


        IS-IS process: test VRF: VRF1
        loopback1, Interface status: protocol-up/link-up/admin-up
        IP address: 77.77.77.77, IP subnet: 77.77.77.77/32
        IPv6 address:
            2001:db8:77:77:77::77/128 [VALID]
        IPv6 subnet:  2001:db8:77:77:77::77/128
        IPv6 link-local address: fe80::5c00:40ff:fe06:0
        Level1
            No auth type and keychain
            Auth check set
        Level2
            No auth type and keychain
            Auth check set
        Index: 0x0002, Local Circuit ID: 0x01, Circuit Type: L1-2
        BFD IPv4 is locally disabled for Interface loopback1
        BFD IPv6 is locally disabled for Interface loopback1
        MTR is enabled
        Level      Metric
        1               1
        2               1
        Topologies enabled:
            L  MT  Metric  MetricCfg  Fwdng IPV4-MT  IPV4Cfg  IPV6-MT  IPV6Cfg
            1  0        1       no   UP    UP       yes      DN       yes
            1  2        1       no   UP    DN       no       UP       yes
            2  0        1       no   UP    UP       yes      DN       yes
            2  2        1       no   UP    DN       no       UP       yes

        Ethernet1/5, Interface status: protocol-up/link-up/admin-up
        IP address: 20.2.7.7, IP subnet: 20.2.7.0/24
        IPv6 address:
            2001:db8:20:2:7::7/64 [VALID]
        IPv6 subnet:  2001:db8:20:2::/64
        IPv6 link-local address: fe80::5c00:40ff:fe06:7
        Level1
            No auth type and keychain
            Auth check set
        Level2
            No auth type and keychain
            Auth check set
        Index: 0x0001, Local Circuit ID: 0x01, Circuit Type: L1-2
        BFD IPv4 is locally disabled for Interface Ethernet1/5
        BFD IPv6 is locally disabled for Interface Ethernet1/5
        MTR is enabled
        LSP interval: 33 ms, MTU: 1500
        Level-2 Designated IS: R2
        Level   Metric-0   Metric-2   CSNP  Next CSNP  Hello   Multi   Next IIH
        1              40     40     10 Inactive      10   3       00:00:02
        2              40     40     10 00:00:04      10   3       00:00:08
        Level  Adjs   AdjsUp Pri  Circuit ID         Since
        1         0        0  64  R7.01              never
        2         1        1  64  R2.01              1w0d
        Topologies enabled:
            L  MT  Metric  MetricCfg  Fwdng IPV4-MT  IPV4Cfg  IPV6-MT  IPV6Cfg
            1  0        40      no   UP    UP       yes      DN       yes
            1  2        40      no   UP    DN       no       UP       yes
            2  0        40      no   UP    UP       yes      DN       yes
            2  2        40      no   UP    DN       no       UP       yes
    '''

    showIsisAdjacencyVrfAll = '''\
        show isis adjacency vrf all
        IS-IS process: test VRF: default
        IS-IS adjacency database:
        Legend: '!': No AF level connectivity in given topology
        System ID       SNPA            Level  State  Hold Time  Interface
        R5              fa16.3ed0.46fc  1      UP     00:00:08   Ethernet1/1
        R5              fa16.3ed0.46fc  2      UP     00:00:09   Ethernet1/1
        R6              5e00.4005.0007  1      UP     00:00:30   Ethernet1/2
        R8              fa16.3eed.aa40  2      UP     00:00:08   Ethernet1/3
        R9              fa16.3e06.ce8d  2      UP     00:00:09   Ethernet1/4

        IS-IS process: test VRF: VRF1
        IS-IS adjacency database:
        Legend: '!': No AF level connectivity in given topology
        System ID       SNPA            Level  State  Hold Time  Interface
        R2              fa16.3e63.eab0  2      UP     00:00:09   Ethernet1/5
    '''

    showIsisHostnameDetailVrfAll = '''\
        show isis hostname detail vrf all
        IS-IS Process: test dynamic hostname table VRF: default
        Level  LSP ID                Dynamic hostname
        2      2222.2222.2222.00-00  R2
        1      3333.3333.3333.00-00  R3
        2      3333.3333.3333.00-00  R3
        1      4444.4444.4444.00-00  R4
        1      5555.5555.5555.00-00  R5
        2      5555.5555.5555.00-00  R5
        1      6666.6666.6666.00-00  R6
        1      7777.7777.7777.00-00* R7
        2      7777.7777.7777.00-00* R7
        2      8888.8888.8888.00-00  R8
        2      9999.9999.9999.00-00  R9

        IS-IS Process: test dynamic hostname table VRF: VRF1
        Level  LSP ID                Dynamic hostname
        2      2222.2222.2222.00-00  R2
        1      7777.7777.7777.00-00* R7
        2      7777.7777.7777.00-00* R7
    '''

    showIsisDatabaseDetail = '''\
        show isis database detail
        IS-IS Process: test LSP database VRF: default
        IS-IS Level-1 Link State Database
        LSPID                 Seq Number   Checksum  Lifetime   A/P/O/T
        R3.00-00              0x00000354   0xD12B    712        1/0/0/3
            Instance      :  0x0000034F
            Area Address  :  49.0002
            Extended IS   :  R3.01              Metric : 10
            Extended IS   :  R4.03              Metric : 10
            Extended IS   :  R3.05              Metric : 10
            NLPID         :  0xCC 0x8E
            IP Address    :  3.3.3.3
            Extended IP   :         3.3.3.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.2.3.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.4.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.5.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.6.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Hostname      :  R3                 Length : 2
            TopoId: 2
            MtExtend IS   :  R3.01              Metric : 10
                            R4.03              Metric : 10
                            R3.05              Metric : 10
            IPv6 Address  :  2001:db8:3:3:3::3
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:3:3:3::3/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:2::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:3::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:16386 Att: 0 Ol: 0
            Digest Offset :  0
        R3.01-00              0x00000352   0xEF24    866        0/0/0/3
            Instance      :  0x00000351
            Extended IS   :  R3.00              Metric : 0
            Extended IS   :  R5.00              Metric : 0
            Digest Offset :  0
        R3.05-00              0x0000034D   0xDDD0    676        0/0/0/3
            Instance      :  0x0000034C
            Extended IS   :  R3.00              Metric : 0
            Extended IS   :  R6.00              Metric : 0
            Digest Offset :  0
        R4.00-00              0x00000353   0x4A65    778        0/0/0/1
            Instance      :  0x0000034F
            Area Address  :  49.0002
            Extended IS   :  R4.03              Metric : 10
            Extended IS   :  R5.02              Metric : 10
            NLPID         :  0xCC 0x8E
            IP Address    :  4.4.4.4
            Extended IP   :         4.4.4.4/32  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.4.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.4.5.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Hostname      :  R4                 Length : 2
            TopoId: 2
            MtExtend IS   :  R4.03              Metric : 10
                            R5.02              Metric : 10
            IPv6 Address  :  2001:db8:4:4:4::4
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:4:4:4::4/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:3::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:4::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:2 Att: 0 Ol: 0
            Digest Offset :  0
        R4.03-00              0x0000034B   0x54C6    902        0/0/0/1
            Instance      :  0x0000034A
            Extended IS   :  R4.00              Metric : 0
            Extended IS   :  R3.00              Metric : 0
            Digest Offset :  0
        R5.00-00              0x0000034D   0xDFA6    984        1/0/0/3
            Instance      :  0x0000034B
            Area Address  :  49.0002
            NLPID         :  0xCC 0x8E
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:16386 Att: 0 Ol: 0
            Hostname      :  R5                 Length : 2
            Extended IS   :  R5.03              Metric : 10
            Extended IS   :  R3.01              Metric : 10
            Extended IS   :  R5.02              Metric : 10
            TopoId: 2
            MtExtend IS   :  R5.03              Metric : 10
                            R3.01              Metric : 10
                            R5.02              Metric : 10
            IP Address    :  5.5.5.5
            Extended IP   :         5.5.5.5/32  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.5.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.4.5.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.5.7.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            IPv6 Address  :  2001:db8:5:5:5::5
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:5:5:5::5/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:3::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:4::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:5::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Digest Offset :  0
        R5.02-00              0x0000034E   0xA5B5    651        0/0/0/3
            Instance      :  0x0000034D
            Extended IS   :  R5.00              Metric : 0
            Extended IS   :  R4.00              Metric : 0
            Digest Offset :  0
        R5.03-00              0x0000034F   0x9C89    897        0/0/0/3
            Instance      :  0x0000034E
            Extended IS   :  R5.00              Metric : 0
            Extended IS   :  R7.00              Metric : 0
            Digest Offset :  0
        R6.00-00              0x000004B3   0xA52C    987        0/0/0/1
            Instance      :  0x000004B1
            Area Address  :  49.0002
            NLPID         :  0xCC 0x8E
            Router ID     :  6.6.6.6
            IP Address    :  6.6.6.6
            MT TopoId     : TopoId:2 Att: 0 Ol: 0
                            TopoId:0 Att: 0 Ol: 0
            Hostname      :  R6                 Length : 2
            TopoId: 2
            MtExtend IS   :  R3.05              Metric : 40
                            R7.02              Metric : 40
            Extended IS   :  R3.05              Metric : 40
            Extended IS   :  R7.02              Metric : 40
            Extended IP   :         6.6.6.0/24  Metric : 1           (U)
            Extended IP   :        10.6.7.0/24  Metric : 40          (U)
            Extended IP   :        10.3.6.0/24  Metric : 40          (U)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:6:6:6::6/128  Metric : 1           (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:6::/64  Metric : 40          (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:3::/64  Metric : 40          (U/I)
            Digest Offset :  0
        R7.00-00            * 0x000004B6   0x425F    787        1/0/0/3
            Instance      :  0x000004B6
            Area Address  :  49.0002
            NLPID         :  0xCC 0x8E
            Router ID     :  7.7.7.7
            IP Address    :  7.7.7.7
            MT TopoId     : TopoId:2 Att: 0 Ol: 0
                            TopoId:0 Att: 0 Ol: 0
            Hostname      :  R7                 Length : 2
            TopoId: 2
            MtExtend IS   :  R7.02              Metric : 40
                            R5.03              Metric : 40
            Extended IS   :  R7.02              Metric : 40
            Extended IS   :  R5.03              Metric : 40
            Extended IP   :        10.7.8.0/24  Metric : 40          (D)
            Extended IP   :         7.7.7.7/32  Metric : 1           (U)
            Extended IP   :        10.7.9.0/24  Metric : 40          (U)
            Extended IP   :        10.6.7.0/24  Metric : 40          (U)
            Extended IP   :        10.5.7.0/24  Metric : 40          (U)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:7::/64  Metric : 40          (D/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:7:7:7::7/128  Metric : 1           (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:77::/64  Metric : 40          (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:6::/64  Metric : 40          (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:5::/64  Metric : 40          (U/I)
            Digest Offset :  0
        R7.02-00            * 0x000004B2   0x25F2    697        0/0/0/3
            Instance      :  0x000004B2
            Extended IS   :  R6.00              Metric : 0
            Extended IS   :  R7.00              Metric : 0
            Digest Offset :  0

        IS-IS Level-2 Link State Database
        LSPID                 Seq Number   Checksum  Lifetime   A/P/O/T
        R2.00-00              0x00000351   0x4E40    870        0/0/0/3
            Instance      :  0x0000034D
            Area Address  :  49.0001
            NLPID         :  0xCC 0x8E
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:2 Att: 0 Ol: 0
            Hostname      :  R2                 Length : 2
            Extended IS   :  R3.07              Metric : 10
            TopoId: 2
            MtExtend IS   :  R3.07              Metric : 10
            IP Address    :  2.2.2.2
            Extended IP   :         2.2.2.2/32  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.1.2.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.2.3.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         1.1.1.1/32  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            IPv6 Address  :  2001:db8:2:2:2::2
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:2:2:2::2/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:1:1:1::1/128  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:1::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:2::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Digest Offset :  0
        R3.00-00              0x00000359   0xC91D    618        0/0/0/3
            Instance      :  0x00000353
            Area Address  :  49.0002
            Extended IS   :  R3.01              Metric : 10
            Extended IS   :  R3.07              Metric : 10
            NLPID         :  0xCC 0x8E
            IP Address    :  3.3.3.3
            Extended IP   :         3.3.3.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.2.3.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.4.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.5.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.6.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         4.4.4.4/32  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         5.5.5.5/32  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.4.5.0/24  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.5.7.0/24  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         7.7.7.7/32  Metric : 21          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.7.9.0/24  Metric : 60          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.6.7.0/24  Metric : 50          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         6.6.6.0/24  Metric : 11          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Hostname      :  R3                 Length : 2
            TopoId: 2
            MtExtend IS   :  R3.01              Metric : 10
                            R3.07              Metric : 10
            IPv6 Address  :  2001:db8:3:3:3::3
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:3:3:3::3/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:2::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:3::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:4:4:4::4/128  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:5:5:5::5/128  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:4::/64  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:5::/64  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:7:7:7::7/128  Metric : 21          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:77::/64  Metric : 60          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:6:6:6::6/128  Metric : 11          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:6::/64  Metric : 50          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:2 Att: 0 Ol: 0
            Digest Offset :  0
        R3.01-00              0x0000034F   0xF521    712        0/0/0/3
            Instance      :  0x0000034E
            Extended IS   :  R3.00              Metric : 0
            Extended IS   :  R5.00              Metric : 0
            Digest Offset :  0
        R3.07-00              0x00000351   0xC77A    1086       0/0/0/3
            Instance      :  0x00000350
            Extended IS   :  R3.00              Metric : 0
            Extended IS   :  R2.00              Metric : 0
            Digest Offset :  0
        R5.00-00              0x00000353   0xC9D4    606        0/0/0/3
            Instance      :  0x00000351
            Area Address  :  49.0002
            NLPID         :  0xCC 0x8E
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:2 Att: 0 Ol: 0
            Hostname      :  R5                 Length : 2
            Extended IS   :  R5.03              Metric : 10
            Extended IS   :  R3.01              Metric : 10
            TopoId: 2
            MtExtend IS   :  R5.03              Metric : 10
                            R3.01              Metric : 10
            IP Address    :  5.5.5.5
            Extended IP   :         5.5.5.5/32  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.5.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.4.5.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.5.7.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         7.7.7.7/32  Metric : 11          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.7.9.0/24  Metric : 50          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.6.7.0/24  Metric : 50          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         4.4.4.4/32  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.4.0/24  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         3.3.3.0/24  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.2.3.0/24  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.3.6.0/24  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :         6.6.6.0/24  Metric : 21          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            IPv6 Address  :  2001:db8:5:5:5::5
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:5:5:5::5/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:3::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:4::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:5::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:7:7:7::7/128  Metric : 11          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:6::/64  Metric : 50          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:77::/64  Metric : 50          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:3:3:3::3/128  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:4:4:4::4/128  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:2::/64  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:6:6:6::6/128  Metric : 21          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Digest Offset :  0
        R5.03-00              0x0000034E   0xB6F8    642        0/0/0/3
            Instance      :  0x0000034D
            Extended IS   :  R5.00              Metric : 0
            Extended IS   :  R7.00              Metric : 0
            Digest Offset :  0
        R7.00-00            * 0x000004B5   0x59EB    926        0/0/0/3
            Instance      :  0x000004B5
            Area Address  :  49.0002
            NLPID         :  0xCC 0x8E
            Router ID     :  7.7.7.7
            IP Address    :  7.7.7.7
            MT TopoId     : TopoId:2 Att: 0 Ol: 0
                            TopoId:0 Att: 0 Ol: 0
            Hostname      :  R7                 Length : 2
            TopoId: 2
            MtExtend IS   :  R5.03              Metric : 40
                            R9.01              Metric : 40
                            R8.01              Metric : 40
            Extended IS   :  R5.03              Metric : 40
            Extended IS   :  R9.01              Metric : 40
            Extended IS   :  R8.01              Metric : 40
            Extended IP   :        10.6.7.0/24  Metric : 40          (U)
            Extended IP   :         7.7.7.7/32  Metric : 1           (U)
            Extended IP   :        10.7.9.0/24  Metric : 40          (U)
            Extended IP   :        10.7.8.0/24  Metric : 40          (U)
            Extended IP   :        10.5.7.0/24  Metric : 40          (U)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:6::/64  Metric : 40          (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:7:7:7::7/128  Metric : 1           (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:77::/64  Metric : 40          (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:7::/64  Metric : 40          (U/I)
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:10:5::/64  Metric : 40          (U/I)
            Digest Offset :  0
        R8.00-00              0x0000034E   0x7758    1116       0/0/0/3
            Instance      :  0x0000034C
            Area Address  :  49.0003
            NLPID         :  0xCC 0x8E
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:2 Att: 0 Ol: 0
            Hostname      :  R8                 Length : 2
            Extended IS   :  R8.01              Metric : 10
            TopoId: 2
            MtExtend IS   :  R8.01              Metric : 10
            IP Address    :  8.8.8.8
            Extended IP   :         8.8.8.8/32  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.7.8.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            IPv6 Address  :  2001:db8:8:8:8::8
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:8:8:8::8/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:7::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Digest Offset :  0
        R8.01-00              0x0000034E   0xF753    770        0/0/0/3
            Instance      :  0x0000034D
            Extended IS   :  R8.00              Metric : 0
            Extended IS   :  R7.00              Metric : 0
            Digest Offset :  0
        R9.00-00              0x0000034A   0x6C98    871        0/0/0/3
            Instance      :  0x00000347
            Area Address  :  49.0004
            NLPID         :  0xCC 0x8E
            MT TopoId     : TopoId:0 Att: 0 Ol: 0
                            TopoId:2 Att: 0 Ol: 0
            Hostname      :  R9                 Length : 2
            Extended IS   :  R9.01              Metric : 10
            TopoId: 2
            MtExtend IS   :  R9.01              Metric : 10
            IP Address    :  9.9.9.9
            Extended IP   :         9.9.9.9/32  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :        10.7.9.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :       10.9.10.0/24  Metric : 10          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Extended IP   :     10.10.10.10/32  Metric : 20          (U)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            IPv6 Address  :  2001:db8:9:9:9::9
            MT-IPv6 Prefx :  TopoId : 2
                            2001:db8:9:9:9::9/128  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:7::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:9::/64  Metric : 10          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
        2001:db8:10:10:10::10/128  Metric : 20          (U/I)
            Unknown Sub-TLV      :  Length : 1  Type :   4
            Digest Offset :  0
        R9.01-00              0x00000352   0x5624    718        0/0/0/3
            Instance      :  0x00000351
            Extended IS   :  R9.00              Metric : 0
            Extended IS   :  R7.00              Metric : 0
            Digest Offset :  0
    '''

    isisOpsOutput = {
        'instance': {
            'test': {
                'process_id': 'test',
                'vrf': {
                    'VRF1': {
                        'area_address': ['49.0002'],
                        'enable': True,
                        'graceful_restart': {
                            'enable': True,
                        },
                        'hostname_db': {
                            'hostname': {
                                '2222.2222.2222.00-00': {
                                    'hostname': 'R2',
                                },
                                '7777.7777.7777.00-00': {
                                    'hostname': 'R7',
                                },
                            },
                        },
                        'interfaces': {
                            'Ethernet1/5': {
                                'adjacencies': {
                                    'R2': {
                                        'neighbor_snpa': {
                                            'fa16.3e63.eab0': {
                                                'level': {
                                                    'level-2': {
                                                        'hold_timer': 9,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 10,
                                    },
                                    'level_2': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_1': {
                                        'multiplier': 3,
                                    },
                                    'level_2': {
                                        'multiplier': 3,
                                    },
                                },
                                'level_type': 'level-1-2',
                                'lsp_pacing_interval': 33,
                                'name': 'Ethernet1/5',
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    '0': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '0',
                                    },
                                    '2': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '2',
                                    },
                                },
                            },
                            'loopback1': {
                                'level_type': 'level-1-2',
                                'name': 'loopback1',
                                'topologies': {
                                    '0': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 1,
                                            },
                                            'level_2': {
                                                'metric': 1,
                                            },
                                        },
                                        'name': '0',
                                    },
                                    '2': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 1,
                                            },
                                            'level_2': {
                                                'metric': 1,
                                            },
                                        },
                                        'name': '2',
                                    },
                                },
                            },
                        },
                        'lsp_mtu': 1492,
                        'metric_type': {
                            'value': 'wide-only',
                        },
                        'system_id': '7777.7777.7777',
                        'topologies': {
                            '0': {
                                'preference': {
                                    'coarse': {
                                        'default': 115,
                                    },
                                },
                                'topology': '0',
                            },
                            '2': {
                                'preference': {
                                    'coarse': {
                                        'default': 115,
                                    },
                                },
                                'topology': '2',
                            },
                        },
                        'vrf': 'VRF1',
                    },
                    'default': {
                        'area_address': ['49.0002'],
                        'enable': True,
                        'graceful_restart': {
                            'enable': True,
                        },
                        'hostname_db': {
                            'hostname': {
                                '2222.2222.2222.00-00': {
                                    'hostname': 'R2',
                                },
                                '3333.3333.3333.00-00': {
                                    'hostname': 'R3',
                                },
                                '4444.4444.4444.00-00': {
                                    'hostname': 'R4',
                                },
                                '5555.5555.5555.00-00': {
                                    'hostname': 'R5',
                                },
                                '6666.6666.6666.00-00': {
                                    'hostname': 'R6',
                                },
                                '7777.7777.7777.00-00': {
                                    'hostname': 'R7',
                                },
                                '8888.8888.8888.00-00': {
                                    'hostname': 'R8',
                                },
                                '9999.9999.9999.00-00': {
                                    'hostname': 'R9',
                                },
                            },
                        },
                        'interfaces': {
                            'Ethernet1/1': {
                                'adjacencies': {
                                    'R5': {
                                        'neighbor_snpa': {
                                            'fa16.3ed0.46fc': {
                                                'level': {
                                                    'level-1': {
                                                        'hold_timer': 8,
                                                        'state': 'Up',
                                                    },
                                                    'level-2': {
                                                        'hold_timer': 9,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 10,
                                    },
                                    'level_2': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_1': {
                                        'multiplier': 3,
                                    },
                                    'level_2': {
                                        'multiplier': 3,
                                    },
                                },
                                'level_type': 'level-1-2',
                                'lsp_pacing_interval': 33,
                                'name': 'Ethernet1/1',
                                'passive': True,
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    '0': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '0',
                                    },
                                    '2': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '2',
                                    },
                                },
                            },
                            'Ethernet1/2': {
                                'adjacencies': {
                                    'R6': {
                                        'neighbor_snpa': {
                                            '5e00.4005.0007': {
                                                'level': {
                                                    'level-1': {
                                                        'hold_timer': 30,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_2': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_2': {
                                        'multiplier': 3,
                                    },
                                },
                                'level_type': 'level-1-only',
                                'lsp_pacing_interval': 33,
                                'name': 'Ethernet1/2',
                                'priority': {
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    '0': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '0',
                                    },
                                    '2': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '2',
                                    },
                                },
                            },
                            'Ethernet1/3': {
                                'adjacencies': {
                                    'R8': {
                                        'neighbor_snpa': {
                                            'fa16.3eed.aa40': {
                                                'level': {
                                                    'level-2': {
                                                        'hold_timer': 8,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 10,
                                    },
                                    'level_2': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_1': {
                                        'multiplier': 3,
                                    },
                                    'level_2': {
                                        'multiplier': 3,
                                    },
                                },
                                'level_type': 'level-2-only',
                                'lsp_pacing_interval': 33,
                                'name': 'Ethernet1/3',
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    '0': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '0',
                                    },
                                    '2': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '2',
                                    },
                                },
                            },
                            'Ethernet1/4': {
                                'adjacencies': {
                                    'R9': {
                                        'neighbor_snpa': {
                                            'fa16.3e06.ce8d': {
                                                'level': {
                                                    'level-2': {
                                                        'hold_timer': 9,
                                                        'state': 'Up',
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                'hello_interval': {
                                    'level_1': {
                                        'interval': 10,
                                    },
                                },
                                'hello_multiplier': {
                                    'level_1': {
                                        'multiplier': 3,
                                    },
                                },
                                'level_type': 'level-1-2',
                                'lsp_pacing_interval': 33,
                                'name': 'Ethernet1/4',
                                'priority': {
                                    'level_1': {
                                        'priority': 64,
                                    },
                                    'level_2': {
                                        'priority': 64,
                                    },
                                },
                                'topologies': {
                                    '0': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '0',
                                    },
                                    '2': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 40,
                                            },
                                            'level_2': {
                                                'metric': 40,
                                            },
                                        },
                                        'name': '2',
                                    },
                                },
                            },
                            'loopback0': {
                                'level_type': 'level-1-2',
                                'name': 'loopback0',
                                'topologies': {
                                    '0': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 1,
                                            },
                                            'level_2': {
                                                'metric': 1,
                                            },
                                        },
                                        'name': '0',
                                    },
                                    '2': {
                                        'metric': {
                                            'level_1': {
                                                'metric': 1,
                                            },
                                            'level_2': {
                                                'metric': 1,
                                            },
                                        },
                                        'name': '2',
                                    },
                                },
                            },
                        },
                        'lsp_mtu': 1492,
                        'metric_type': {
                            'value': 'wide-only',
                        },
                        'system_id': '7777.7777.7777',
                        'topologies': {
                            '0': {
                                'preference': {
                                    'coarse': {
                                        'default': 115,
                                    },
                                },
                                'topology': '0',
                            },
                            '2': {
                                'preference': {
                                    'coarse': {
                                        'default': 115,
                                    },
                                },
                                'topology': '2',
                            },
                        },
                        'vrf': 'default',
                    },
                },
            },
        },
    }

    isisLsdbOpsOutput = {
        'instance': {
            'test': {
                'vrf': {
                    'default': {
                        'level_db': {
                            1: {
                                'R3.00-00': {
                                    'checksum': '0xD12B',
                                    'dynamic_hostname': 'R3',
                                    'extended_ipv4_reachability': {
                                        '10.2.3.0/24': {
                                            'ip_prefix': '10.2.3.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.4.0/24': {
                                            'ip_prefix': '10.3.4.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.5.0/24': {
                                            'ip_prefix': '10.3.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.6.0/24': {
                                            'ip_prefix': '10.3.6.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '3.3.3.0/24': {
                                            'ip_prefix': '3.3.3.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R3.05': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.05',
                                        },
                                        'R4.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R4.03',
                                        },
                                    },
                                    'ipv4_addresses': ['3.3.3.3'],
                                    'ipv6_addresses': ['2001:db8:3:3:3::3'],
                                    'lsp_id': 'R3.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '16386': {
                                            'attributes': '0',
                                            'mt_id': '16386',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:2::/64': {
                                            'ip_prefix': '2001:db8:10:2::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:3:3:3::3/128': {
                                            'ip_prefix': '2001:db8:3:3:3::3',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R3.05': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R3.05',
                                        },
                                    },
                                    'remaining_lifetime': 712,
                                    'sequence': '0x00000354',
                                },
                                'R3.01-00': {
                                    'checksum': '0xEF24',
                                    'extended_is_neighbor': {
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                    },
                                    'lsp_id': 'R3.01-00',
                                    'remaining_lifetime': 866,
                                    'sequence': '0x00000352',
                                },
                                'R3.05-00': {
                                    'checksum': '0xDDD0',
                                    'extended_is_neighbor': {
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                        'R6.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R6.00',
                                        },
                                    },
                                    'lsp_id': 'R3.05-00',
                                    'remaining_lifetime': 676,
                                    'sequence': '0x0000034D',
                                },
                                'R4.00-00': {
                                    'checksum': '0x4A65',
                                    'dynamic_hostname': 'R4',
                                    'extended_ipv4_reachability': {
                                        '10.3.4.0/24': {
                                            'ip_prefix': '10.3.4.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.4.5.0/24': {
                                            'ip_prefix': '10.4.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '4.4.4.4/32': {
                                            'ip_prefix': '4.4.4.4',
                                            'metric': 10,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R4.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R4.03',
                                        },
                                        'R5.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R5.02',
                                        },
                                    },
                                    'ipv4_addresses': ['4.4.4.4'],
                                    'ipv6_addresses': ['2001:db8:4:4:4::4'],
                                    'lsp_id': 'R4.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:4::/64': {
                                            'ip_prefix': '2001:db8:10:4::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:4:4:4::4/128': {
                                            'ip_prefix': '2001:db8:4:4:4::4',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R5.02': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R5.02',
                                        },
                                    },
                                    'remaining_lifetime': 778,
                                    'sequence': '0x00000353',
                                },
                                'R4.03-00': {
                                    'checksum': '0x54C6',
                                    'extended_is_neighbor': {
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                        'R4.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R4.00',
                                        },
                                    },
                                    'lsp_id': 'R4.03-00',
                                    'remaining_lifetime': 902,
                                    'sequence': '0x0000034B',
                                },
                                'R5.00-00': {
                                    'checksum': '0xDFA6',
                                    'dynamic_hostname': 'R5',
                                    'extended_ipv4_reachability': {
                                        '10.3.5.0/24': {
                                            'ip_prefix': '10.3.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.4.5.0/24': {
                                            'ip_prefix': '10.4.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.5.7.0/24': {
                                            'ip_prefix': '10.5.7.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '5.5.5.5/32': {
                                            'ip_prefix': '5.5.5.5',
                                            'metric': 10,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R5.02': {
                                            'metric': 10,
                                            'neighbor_id': 'R5.02',
                                        },
                                        'R5.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R5.03',
                                        },
                                    },
                                    'ipv4_addresses': ['5.5.5.5'],
                                    'ipv6_addresses': ['2001:db8:5:5:5::5'],
                                    'lsp_id': 'R5.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '16386': {
                                            'attributes': '0',
                                            'mt_id': '16386',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:4::/64': {
                                            'ip_prefix': '2001:db8:10:4::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:5::/64': {
                                            'ip_prefix': '2001:db8:10:5::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:5:5:5::5/128': {
                                            'ip_prefix': '2001:db8:5:5:5::5',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R5.02': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R5.02',
                                        },
                                    },
                                    'remaining_lifetime': 984,
                                    'sequence': '0x0000034D',
                                },
                                'R5.02-00': {
                                    'checksum': '0xA5B5',
                                    'extended_is_neighbor': {
                                        'R4.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R4.00',
                                        },
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                    },
                                    'lsp_id': 'R5.02-00',
                                    'remaining_lifetime': 651,
                                    'sequence': '0x0000034E',
                                },
                                'R5.03-00': {
                                    'checksum': '0x9C89',
                                    'extended_is_neighbor': {
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                        'R7.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R7.00',
                                        },
                                    },
                                    'lsp_id': 'R5.03-00',
                                    'remaining_lifetime': 897,
                                    'sequence': '0x0000034F',
                                },
                                'R6.00-00': {
                                    'checksum': '0xA52C',
                                    'dynamic_hostname': 'R6',
                                    'extended_ipv4_reachability': {
                                        '10.3.6.0/24': {
                                            'ip_prefix': '10.3.6.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.6.7.0/24': {
                                            'ip_prefix': '10.6.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '6.6.6.0/24': {
                                            'ip_prefix': '6.6.6.0',
                                            'metric': 1,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.05': {
                                            'metric': 40,
                                            'neighbor_id': 'R3.05',
                                        },
                                        'R7.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R7.02',
                                        },
                                    },
                                    'ipv4_addresses': ['6.6.6.6'],
                                    'lsp_id': 'R6.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:6::/64': {
                                            'ip_prefix': '2001:db8:10:6::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:6:6:6::6/128': {
                                            'ip_prefix': '2001:db8:6:6:6::6',
                                            'metric': 1,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R7.00': {
                                            'metric': 40,
                                            'mt_id': '2',
                                            'neighbor_id': 'R7.02',
                                        },
                                    },
                                    'remaining_lifetime': 987,
                                    'sequence': '0x000004B3',
                                },
                                'R7.00-00': {
                                    'checksum': '0x425F',
                                    'dynamic_hostname': 'R7',
                                    'extended_ipv4_reachability': {
                                        '10.5.7.0/24': {
                                            'ip_prefix': '10.5.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.6.7.0/24': {
                                            'ip_prefix': '10.6.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.7.8.0/24': {
                                            'ip_prefix': '10.7.8.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': False,
                                        },
                                        '10.7.9.0/24': {
                                            'ip_prefix': '10.7.9.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '7.7.7.7/32': {
                                            'ip_prefix': '7.7.7.7',
                                            'metric': 1,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R5.03': {
                                            'metric': 40,
                                            'neighbor_id': 'R5.03',
                                        },
                                        'R7.02': {
                                            'metric': 40,
                                            'neighbor_id': 'R7.02',
                                        },
                                    },
                                    'ipv4_addresses': ['7.7.7.7'],
                                    'lsp_id': 'R7.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:5::/64': {
                                            'ip_prefix': '2001:db8:10:5::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:6::/64': {
                                            'ip_prefix': '2001:db8:10:6::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:77::/64': {
                                            'ip_prefix': '2001:db8:10:77::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:7::/64': {
                                            'ip_prefix': '2001:db8:10:7::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': False,
                                        },
                                        '2001:db8:7:7:7::7/128': {
                                            'ip_prefix': '2001:db8:7:7:7::7',
                                            'metric': 1,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R7.02': {
                                            'metric': 40,
                                            'mt_id': '2',
                                            'neighbor_id': 'R5.03',
                                        },
                                    },
                                    'remaining_lifetime': 787,
                                    'sequence': '0x000004B6',
                                },
                                'R7.02-00': {
                                    'checksum': '0x25F2',
                                    'extended_is_neighbor': {
                                        'R6.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R6.00',
                                        },
                                        'R7.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R7.00',
                                        },
                                    },
                                    'lsp_id': 'R7.02-00',
                                    'remaining_lifetime': 697,
                                    'sequence': '0x000004B2',
                                },
                            },
                            2: {
                                'R2.00-00': {
                                    'checksum': '0x4E40',
                                    'dynamic_hostname': 'R2',
                                    'extended_ipv4_reachability': {
                                        '1.1.1.1/32': {
                                            'ip_prefix': '1.1.1.1',
                                            'metric': 20,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                        '10.1.2.0/24': {
                                            'ip_prefix': '10.1.2.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.2.3.0/24': {
                                            'ip_prefix': '10.2.3.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '2.2.2.2/32': {
                                            'ip_prefix': '2.2.2.2',
                                            'metric': 10,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.07': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.07',
                                        },
                                    },
                                    'ipv4_addresses': ['2.2.2.2'],
                                    'ipv6_addresses': ['2001:db8:2:2:2::2'],
                                    'lsp_id': 'R2.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:1::/64': {
                                            'ip_prefix': '2001:db8:10:1::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:2::/64': {
                                            'ip_prefix': '2001:db8:10:2::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:1:1:1::1/128': {
                                            'ip_prefix': '2001:db8:1:1:1::1',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:2:2:2::2/128': {
                                            'ip_prefix': '2001:db8:2:2:2::2',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R3.07': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R3.07',
                                        },
                                    },
                                    'remaining_lifetime': 870,
                                    'sequence': '0x00000351',
                                },
                                'R3.00-00': {
                                    'checksum': '0xC91D',
                                    'dynamic_hostname': 'R3',
                                    'extended_ipv4_reachability': {
                                        '10.2.3.0/24': {
                                            'ip_prefix': '10.2.3.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.4.0/24': {
                                            'ip_prefix': '10.3.4.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.5.0/24': {
                                            'ip_prefix': '10.3.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.6.0/24': {
                                            'ip_prefix': '10.3.6.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.4.5.0/24': {
                                            'ip_prefix': '10.4.5.0',
                                            'metric': 20,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.5.7.0/24': {
                                            'ip_prefix': '10.5.7.0',
                                            'metric': 20,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.6.7.0/24': {
                                            'ip_prefix': '10.6.7.0',
                                            'metric': 50,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.7.9.0/24': {
                                            'ip_prefix': '10.7.9.0',
                                            'metric': 60,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '3.3.3.0/24': {
                                            'ip_prefix': '3.3.3.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '4.4.4.4/32': {
                                            'ip_prefix': '4.4.4.4',
                                            'metric': 20,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                        '5.5.5.5/32': {
                                            'ip_prefix': '5.5.5.5',
                                            'metric': 20,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                        '6.6.6.0/24': {
                                            'ip_prefix': '6.6.6.0',
                                            'metric': 11,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '7.7.7.7/32': {
                                            'ip_prefix': '7.7.7.7',
                                            'metric': 21,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R3.07': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.07',
                                        },
                                    },
                                    'ipv4_addresses': ['3.3.3.3'],
                                    'ipv6_addresses': ['2001:db8:3:3:3::3'],
                                    'lsp_id': 'R3.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:2::/64': {
                                            'ip_prefix': '2001:db8:10:2::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:4::/64': {
                                            'ip_prefix': '2001:db8:10:4::',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:5::/64': {
                                            'ip_prefix': '2001:db8:10:5::',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:6::/64': {
                                            'ip_prefix': '2001:db8:10:6::',
                                            'metric': 50,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:77::/64': {
                                            'ip_prefix': '2001:db8:10:77::',
                                            'metric': 60,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:3:3:3::3/128': {
                                            'ip_prefix': '2001:db8:3:3:3::3',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:4:4:4::4/128': {
                                            'ip_prefix': '2001:db8:4:4:4::4',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:5:5:5::5/128': {
                                            'ip_prefix': '2001:db8:5:5:5::5',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:6:6:6::6/128': {
                                            'ip_prefix': '2001:db8:6:6:6::6',
                                            'metric': 11,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:7:7:7::7/128': {
                                            'ip_prefix': '2001:db8:7:7:7::7',
                                            'metric': 21,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R3.07': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R3.07',
                                        },
                                    },
                                    'remaining_lifetime': 618,
                                    'sequence': '0x00000359',
                                },
                                'R3.01-00': {
                                    'checksum': '0xF521',
                                    'extended_is_neighbor': {
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                    },
                                    'lsp_id': 'R3.01-00',
                                    'remaining_lifetime': 712,
                                    'sequence': '0x0000034F',
                                },
                                'R3.07-00': {
                                    'checksum': '0xC77A',
                                    'extended_is_neighbor': {
                                        'R2.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R2.00',
                                        },
                                        'R3.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R3.00',
                                        },
                                    },
                                    'lsp_id': 'R3.07-00',
                                    'remaining_lifetime': 1086,
                                    'sequence': '0x00000351',
                                },
                                'R5.00-00': {
                                    'checksum': '0xC9D4',
                                    'dynamic_hostname': 'R5',
                                    'extended_ipv4_reachability': {
                                        '10.2.3.0/24': {
                                            'ip_prefix': '10.2.3.0',
                                            'metric': 20,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.4.0/24': {
                                            'ip_prefix': '10.3.4.0',
                                            'metric': 20,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.5.0/24': {
                                            'ip_prefix': '10.3.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.3.6.0/24': {
                                            'ip_prefix': '10.3.6.0',
                                            'metric': 20,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.4.5.0/24': {
                                            'ip_prefix': '10.4.5.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.5.7.0/24': {
                                            'ip_prefix': '10.5.7.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.6.7.0/24': {
                                            'ip_prefix': '10.6.7.0',
                                            'metric': 50,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.7.9.0/24': {
                                            'ip_prefix': '10.7.9.0',
                                            'metric': 50,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '3.3.3.0/24': {
                                            'ip_prefix': '3.3.3.0',
                                            'metric': 20,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '4.4.4.4/32': {
                                            'ip_prefix': '4.4.4.4',
                                            'metric': 20,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                        '5.5.5.5/32': {
                                            'ip_prefix': '5.5.5.5',
                                            'metric': 10,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                        '6.6.6.0/24': {
                                            'ip_prefix': '6.6.6.0',
                                            'metric': 21,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '7.7.7.7/32': {
                                            'ip_prefix': '7.7.7.7',
                                            'metric': 11,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R3.01',
                                        },
                                        'R5.03': {
                                            'metric': 10,
                                            'neighbor_id': 'R5.03',
                                        },
                                    },
                                    'ipv4_addresses': ['5.5.5.5'],
                                    'ipv6_addresses': ['2001:db8:5:5:5::5'],
                                    'lsp_id': 'R5.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:2::/64': {
                                            'ip_prefix': '2001:db8:10:2::',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:3::/64': {
                                            'ip_prefix': '2001:db8:10:3::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:4::/64': {
                                            'ip_prefix': '2001:db8:10:4::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:5::/64': {
                                            'ip_prefix': '2001:db8:10:5::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:6::/64': {
                                            'ip_prefix': '2001:db8:10:6::',
                                            'metric': 50,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:77::/64': {
                                            'ip_prefix': '2001:db8:10:77::',
                                            'metric': 50,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:3:3:3::3/128': {
                                            'ip_prefix': '2001:db8:3:3:3::3',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:4:4:4::4/128': {
                                            'ip_prefix': '2001:db8:4:4:4::4',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:5:5:5::5/128': {
                                            'ip_prefix': '2001:db8:5:5:5::5',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:6:6:6::6/128': {
                                            'ip_prefix': '2001:db8:6:6:6::6',
                                            'metric': 21,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:7:7:7::7/128': {
                                            'ip_prefix': '2001:db8:7:7:7::7',
                                            'metric': 11,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R3.01': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R3.01',
                                        },
                                    },
                                    'remaining_lifetime': 606,
                                    'sequence': '0x00000353',
                                },
                                'R5.03-00': {
                                    'checksum': '0xB6F8',
                                    'extended_is_neighbor': {
                                        'R5.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R5.00',
                                        },
                                        'R7.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R7.00',
                                        },
                                    },
                                    'lsp_id': 'R5.03-00',
                                    'remaining_lifetime': 642,
                                    'sequence': '0x0000034E',
                                },
                                'R7.00-00': {
                                    'checksum': '0x59EB',
                                    'dynamic_hostname': 'R7',
                                    'extended_ipv4_reachability': {
                                        '10.5.7.0/24': {
                                            'ip_prefix': '10.5.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.6.7.0/24': {
                                            'ip_prefix': '10.6.7.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.7.8.0/24': {
                                            'ip_prefix': '10.7.8.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.7.9.0/24': {
                                            'ip_prefix': '10.7.9.0',
                                            'metric': 40,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '7.7.7.7/32': {
                                            'ip_prefix': '7.7.7.7',
                                            'metric': 1,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R5.03': {
                                            'metric': 40,
                                            'neighbor_id': 'R5.03',
                                        },
                                        'R8.01': {
                                            'metric': 40,
                                            'neighbor_id': 'R8.01',
                                        },
                                        'R9.01': {
                                            'metric': 40,
                                            'neighbor_id': 'R9.01',
                                        },
                                    },
                                    'ipv4_addresses': ['7.7.7.7'],
                                    'lsp_id': 'R7.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:5::/64': {
                                            'ip_prefix': '2001:db8:10:5::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:6::/64': {
                                            'ip_prefix': '2001:db8:10:6::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:77::/64': {
                                            'ip_prefix': '2001:db8:10:77::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:7::/64': {
                                            'ip_prefix': '2001:db8:10:7::',
                                            'metric': 40,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:7:7:7::7/128': {
                                            'ip_prefix': '2001:db8:7:7:7::7',
                                            'metric': 1,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R7.00': {
                                            'metric': 40,
                                            'mt_id': '2',
                                            'neighbor_id': 'R8.01',
                                        },
                                    },
                                    'remaining_lifetime': 926,
                                    'sequence': '0x000004B5',
                                },
                                'R8.00-00': {
                                    'checksum': '0x7758',
                                    'dynamic_hostname': 'R8',
                                    'extended_ipv4_reachability': {
                                        '10.7.8.0/24': {
                                            'ip_prefix': '10.7.8.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '8.8.8.8/32': {
                                            'ip_prefix': '8.8.8.8',
                                            'metric': 10,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R8.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R8.01',
                                        },
                                    },
                                    'ipv4_addresses': ['8.8.8.8'],
                                    'ipv6_addresses': ['2001:db8:8:8:8::8'],
                                    'lsp_id': 'R8.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:7::/64': {
                                            'ip_prefix': '2001:db8:10:7::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:8:8:8::8/128': {
                                            'ip_prefix': '2001:db8:8:8:8::8',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R8.01': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R8.01',
                                        },
                                    },
                                    'remaining_lifetime': 1116,
                                    'sequence': '0x0000034E',
                                },
                                'R8.01-00': {
                                    'checksum': '0xF753',
                                    'extended_is_neighbor': {
                                        'R7.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R7.00',
                                        },
                                        'R8.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R8.00',
                                        },
                                    },
                                    'lsp_id': 'R8.01-00',
                                    'remaining_lifetime': 770,
                                    'sequence': '0x0000034E',
                                },
                                'R9.00-00': {
                                    'checksum': '0x6C98',
                                    'dynamic_hostname': 'R9',
                                    'extended_ipv4_reachability': {
                                        '10.10.10.10/32': {
                                            'ip_prefix': '10.10.10.10',
                                            'metric': 20,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                        '10.7.9.0/24': {
                                            'ip_prefix': '10.7.9.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '10.9.10.0/24': {
                                            'ip_prefix': '10.9.10.0',
                                            'metric': 10,
                                            'prefix_len': '24',
                                            'up_down': True,
                                        },
                                        '9.9.9.9/32': {
                                            'ip_prefix': '9.9.9.9',
                                            'metric': 10,
                                            'prefix_len': '32',
                                            'up_down': True,
                                        },
                                    },
                                    'extended_is_neighbor': {
                                        'R9.01': {
                                            'metric': 10,
                                            'neighbor_id': 'R9.01',
                                        },
                                    },
                                    'ipv4_addresses': ['9.9.9.9'],
                                    'ipv6_addresses': ['2001:db8:9:9:9::9'],
                                    'lsp_id': 'R9.00-00',
                                    'mt_entries': {
                                        '0': {
                                            'attributes': '0',
                                            'mt_id': '0',
                                        },
                                        '2': {
                                            'attributes': '0',
                                            'mt_id': '2',
                                        },
                                    },
                                    'mt_ipv6_reachability': {
                                        '2001:db8:10:10:10::10/128': {
                                            'ip_prefix': '2001:db8:10:10:10::10',
                                            'metric': 20,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:7::/64': {
                                            'ip_prefix': '2001:db8:10:7::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:10:9::/64': {
                                            'ip_prefix': '2001:db8:10:9::',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '64',
                                            'up_down': True,
                                        },
                                        '2001:db8:9:9:9::9/128': {
                                            'ip_prefix': '2001:db8:9:9:9::9',
                                            'metric': 10,
                                            'mt_id': '2',
                                            'prefix_len': '128',
                                            'up_down': True,
                                        },
                                    },
                                    'mt_is_neighbor': {
                                        'R9.01': {
                                            'metric': 10,
                                            'mt_id': '2',
                                            'neighbor_id': 'R9.01',
                                        },
                                    },
                                    'remaining_lifetime': 871,
                                    'sequence': '0x0000034A',
                                },
                                'R9.01-00': {
                                    'checksum': '0x5624',
                                    'extended_is_neighbor': {
                                        'R7.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R7.00',
                                        },
                                        'R9.00': {
                                            'metric': 0,
                                            'neighbor_id': 'R9.00',
                                        },
                                    },
                                    'lsp_id': 'R9.01-00',
                                    'remaining_lifetime': 718,
                                    'sequence': '0x00000352',
                                },
                            },
                        },
                    },
                },
            },
        },
    }
